import os
import frontmatter
from markdown import Markdown
from datetime import datetime
from typing import Dict, List, Optional

class ContentValidationError(Exception):
    """Excepción personalizada para errores de validación de contenido"""
    pass

class NoteGenerator:
    REQUIRED_METADATA = ['title', 'date', 'category']
    
    def __init__(self, content_dir: str = 'content'):
        """
        Inicializa el generador de notas.
        
        Args:
            content_dir (str): Directorio donde se encuentran los archivos Markdown
            
        Raises:
            FileNotFoundError: Si el directorio de contenido no existe
        """
        if not os.path.exists(content_dir):
            raise FileNotFoundError(f"El directorio {content_dir} no existe")
        """
        Inicializa el generador de notas.
        
        Args:
            content_dir (str): Directorio donde se encuentran los archivos Markdown
        """
        self.content_dir = content_dir
        self.markdown = Markdown(extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'meta'
        ])
        
    def validate_metadata(self, metadata: Dict, file_path: str) -> Dict:
        """
        Valida y normaliza los metadatos de una nota.
        
        Args:
            metadata (Dict): Metadatos a validar
            file_path (str): Ruta del archivo para mensajes de error
            
        Returns:
            Dict: Metadatos validados y normalizados
            
        Raises:
            ContentValidationError: Si faltan campos requeridos o hay datos inválidos
        """
        for field in self.REQUIRED_METADATA:
            if field not in metadata:
                raise ContentValidationError(f"Campo requerido '{field}' faltante en {file_path}")
        
        # Normalizar fecha
        try:
            if isinstance(metadata['date'], str):
                datetime.strptime(metadata['date'], '%Y-%m-%d')
            elif isinstance(metadata['date'], datetime):
                metadata['date'] = metadata['date'].strftime('%Y-%m-%d')
            else:
                raise ValueError("Formato de fecha inválido")
        except ValueError as e:
            raise ContentValidationError(f"Fecha inválida en {file_path}: {str(e)}")
        
        # Normalizar tags
        if 'tags' in metadata:
            if not isinstance(metadata['tags'], list):
                metadata['tags'] = [tag.strip() for tag in str(metadata['tags']).split(',')]
            metadata['tags'] = [tag.lower() for tag in metadata['tags']]
        else:
            metadata['tags'] = []
            
        return metadata

    def get_note_data(self, file_path: str) -> Dict:
        """
        Lee y procesa un archivo Markdown individual.
        
        Args:
            file_path (str): Ruta al archivo Markdown
            
        Returns:
            Dict: Diccionario con el contenido y metadatos del archivo
            
        Raises:
            ContentValidationError: Si hay problemas con el contenido o metadatos
            FileNotFoundError: Si el archivo no existe
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            post = frontmatter.load(file)
            
        # Procesar el contenido con Markdown
        content = self.markdown.convert(post.content)
        
        # Extraer y validar metadatos
        metadata = post.metadata
        
        # Asegurar campos requeridos
        metadata.setdefault('title', os.path.basename(file_path))
        metadata.setdefault('date', datetime.now().strftime('%Y-%m-%d'))
        metadata.setdefault('category', 'uncategorized')
        metadata.setdefault('tags', [])
        
        # Construir URL relativa
        url = self._generate_url(file_path)
        
        return {
            'content': content,
            'metadata': metadata,
            'url': url,
            'source_path': file_path
        }
    
    def get_all_notes(self) -> List[Dict]:
        """
        Obtiene todas las notas del directorio de contenido.
        
        Returns:
            List[Dict]: Lista de diccionarios con información de cada nota
        """
        notes = []
        for root, _, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        note_data = self.get_note_data(file_path)
                        notes.append(note_data)
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
        
        # Ordenar por fecha descendente
        return sorted(notes, key=lambda x: x['metadata']['date'], reverse=True)
    
    def get_categories(self) -> Dict[str, List[Dict]]:
        """
        Agrupa las notas por categoría.
        
        Returns:
            Dict[str, List[Dict]]: Diccionario de categorías y sus notas
        """
        categories = {}
        for note in self.get_all_notes():
            category = note['metadata']['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(note)
        return categories
    
    def get_tags(self) -> Dict[str, List[Dict]]:
        """
        Agrupa las notas por etiquetas.
        
        Returns:
            Dict[str, List[Dict]]: Diccionario de etiquetas y sus notas
        """
        tags = {}
        for note in self.get_all_notes():
            for tag in note['metadata']['tags']:
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(note)
        return tags
    
    def _generate_url(self, file_path: str) -> str:
        """
        Genera una URL relativa para una nota.
        
        Args:
            file_path (str): Ruta al archivo
            
        Returns:
            str: URL relativa para la nota
        """
        rel_path = os.path.relpath(file_path, self.content_dir)
        return '/' + os.path.splitext(rel_path)[0]

    def get_note_by_url(self, url: str) -> Optional[Dict]:
        """
        Busca una nota por su URL.
        
        Args:
            url (str): URL relativa de la nota
            
        Returns:
            Optional[Dict]: Datos de la nota o None si no se encuentra
        """
        url = url.lstrip('/')
        for note in self.get_all_notes():
            if note['url'].lstrip('/') == url:
                return note
        return None
        
    def search_notes(self, query: str) -> List[Dict]:
        """
        Busca notas por contenido o metadatos.
        
        Args:
            query (str): Término de búsqueda
            
        Returns:
            List[Dict]: Lista de notas que coinciden con la búsqueda
        """
        query = query.lower()
        results = []
        
        for note in self.get_all_notes():
            # Buscar en título
            if query in note['metadata']['title'].lower():
                results.append(note)
                continue
                
            # Buscar en contenido
            if query in note['content'].lower():
                results.append(note)
                continue
                
            # Buscar en tags
            if any(query in tag.lower() for tag in note['metadata']['tags']):
                results.append(note)
                continue
                
        return results
        
    def filter_notes(self, 
                    category: Optional[str] = None,
                    tag: Optional[str] = None,
                    date_from: Optional[str] = None,
                    date_to: Optional[str] = None) -> List[Dict]:
        """
        Filtra notas según varios criterios.
        
        Args:
            category (str, optional): Categoría a filtrar
            tag (str, optional): Tag a filtrar
            date_from (str, optional): Fecha inicial (YYYY-MM-DD)
            date_to (str, optional): Fecha final (YYYY-MM-DD)
            
        Returns:
            List[Dict]: Lista de notas filtradas
        """
        notes = self.get_all_notes()
        
        if category:
            notes = [note for note in notes 
                    if note['metadata']['category'].lower() == category.lower()]
            
        if tag:
            notes = [note for note in notes 
                    if tag.lower() in [t.lower() for t in note['metadata']['tags']]]
            
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            notes = [note for note in notes 
                    if datetime.strptime(note['metadata']['date'], '%Y-%m-%d') >= date_from]
            
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            notes = [note for note in notes 
                    if datetime.strptime(note['metadata']['date'], '%Y-%m-%d') <= date_to]
            
        return notes
        
    def get_related_notes(self, note: Dict, limit: int = 5) -> List[Dict]:
        """
        Encuentra notas relacionadas basadas en categoría y tags.
        
        Args:
            note (Dict): Nota para la cual buscar relacionadas
            limit (int): Número máximo de notas a retornar
            
        Returns:
            List[Dict]: Lista de notas relacionadas
        """
        all_notes = self.get_all_notes()
        related_notes = []
        
        category = note['metadata']['category']
        tags = set(note['metadata']['tags'])
        
        for other_note in all_notes:
            if other_note['url'] == note['url']:
                continue
                
            score = 0
            # Misma categoría
            if other_note['metadata']['category'] == category:
                score += 1
                
            # Tags en común
            other_tags = set(other_note['metadata']['tags'])
            score += len(tags & other_tags)
            
            if score > 0:
                related_notes.append((score, other_note))
                
        # Ordenar por puntuación y limitar resultados
        related_notes.sort(key=lambda x: x[0], reverse=True)
        return [note for score, note in related_notes[:limit]]