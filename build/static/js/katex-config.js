document.addEventListener("DOMContentLoaded", function() {
    // Configuración global de KaTeX
    window.katex = {
        defaultOptions: {
            throwOnError: false,
            errorColor: "#dc2626"
        }
    };

    // Configuración de auto-render
    renderMathInElement(document.body, {
        // Delimitadores para diferentes tipos de expresiones matemáticas
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\[", right: "\\]", display: true },
            { left: "\\(", right: "\\)", display: false },
            { left: "\\begin{equation}", right: "\\end{equation}", display: true },
            { left: "\\begin{align}", right: "\\end{align}", display: true },
            { left: "\\begin{alignat}", right: "\\end{alignat}", display: true },
            { left: "\\begin{gather}", right: "\\end{gather}", display: true },
            { left: "\\begin{CD}", right: "\\end{CD}", display: true }
        ],

        // Opciones de renderizado
        throwOnError: false,
        errorColor: "#dc2626",
        strict: "ignore",
        trust: true,
        strict: false,

        // Macros matemáticos comunes
        macros: {
            // Conjuntos numéricos
            "\\R": "\\mathbb{R}",
            "\\N": "\\mathbb{N}",
            "\\Z": "\\mathbb{Z}",
            "\\Q": "\\mathbb{Q}",
            "\\C": "\\mathbb{C}",
            
            // Operadores comunes
            "\\der": "\\frac{d}{d#1}",  // Derivada
            "\\pder": "\\frac{\\partial}{\\partial#1}", // Derivada parcial
            "\\dx": "\\,dx",
            "\\dy": "\\,dy",
            "\\dz": "\\,dz",
            
            // Vectores y matrices
            "\\vec": "\\mathbf{#1}",
            "\\matrix": "\\begin{pmatrix} #1 \\end{pmatrix}",
            
            // Símbolos especiales
            "\\eps": "\\varepsilon",
            "\\phi": "\\varphi",
            "\\oc": "^\\circ",
            
            // Flechas y relaciones
            "\\impl": "\\Rightarrow",
            "\\iff": "\\Leftrightarrow",
            "\\to": "\\rightarrow",
            
            // Conjuntos y lógica
            "\\set": "\\{#1\\}",
            "\\abs": "\\left|#1\\right|",
            "\\norm": "\\left\\|#1\\right\\|",
            
            // Cálculo
            "\\limit": "\\lim_{#1 \\to #2}",
            "\\sum": "\\sum_{#1}^{#2}",
            "\\integral": "\\int_{#1}^{#2}",
            
            // Probabilidad y estadística
            "\\prob": "\\mathbb{P}\\left(#1\\right)",
            "\\expect": "\\mathbb{E}\\left[#1\\right]",
            "\\var": "\\text{Var}\\left(#1\\right)",
            
            // Espacios y topología
            "\\real": "\\mathbb{R}",
            "\\complex": "\\mathbb{C}",
            "\\field": "\\mathbb{F}",
            
            // Teoría de grupos
            "\\group": "\\mathcal{G}",
            "\\ring": "\\mathcal{R}",
            "\\field": "\\mathcal{F}"
        },

        // Configuración de formato
        output: "html",
        minRuleThickness: 0.05,
        maxSize: Infinity,
        maxExpand: 1000,

        // Características especiales
        fleqn: false,              // Alineación a la izquierda de ecuaciones
        leqno: false,              // Números de ecuación a la izquierda
        displayMode: true,         // Modo display por defecto para bloques
        throwOnError: false,       // No interrumpir en errores
        errorColor: "#dc2626",     // Color rojo para errores
        colorIsTextColor: true,    // Usar color como color de texto

        // Opciones de renderizado adicionales
        strict: false,             // Modo estricto desactivado
        trust: true,              // Permitir comandos potencialmente peligrosos
        wrap: true,               // Permitir saltos de línea en modo inline

        // Manejo de errores personalizado
        errorCallback: function(msg, err) {
            console.warn("KaTeX error:", msg, err);
        }
    });

    // Configuración adicional para elementos específicos
    document.querySelectorAll('.math-display').forEach(function(element) {
        element.style.overflow = 'auto';
        element.style.maxWidth = '100%';
    });

    // Ajustar tamaño de ecuaciones en dispositivos móviles
    function adjustMathSize() {
        const width = window.innerWidth;
        const mathElements = document.querySelectorAll('.katex-display');
        
        mathElements.forEach(function(element) {
            if (width < 768) {
                element.style.fontSize = '90%';
                element.style.overflowX = 'auto';
            } else {
                element.style.fontSize = '100%';
            }
        });
    }

    // Ejecutar ajuste inicial y en cambios de tamaño
    adjustMathSize();
    window.addEventListener('resize', adjustMathSize);
});