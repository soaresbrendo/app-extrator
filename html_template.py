def get_html_template():
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extrator de Pedidos PDF</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container { max-width: 1600px; margin: 0 auto; padding: 20px; }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p { font-size: 1.2rem; opacity: 0.9; }
        
        .card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        
        .card:hover { transform: translateY(-5px); }
        
        .card-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 25px;
        }
        
        .card-header h2 { font-size: 1.5rem; margin-bottom: 8px; }
        .card-header p { opacity: 0.9; font-size: 0.95rem; }
        
        .card-content { padding: 30px; }
        
        .file-upload-area {
            border: 3px dashed #ddd;
            border-radius: 10px;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .file-upload-area:hover {
            border-color: #4facfe;
            background-color: #f8f9ff;
        }
        
        .file-upload-area i {
            font-size: 3rem;
            color: #ddd;
            margin-bottom: 15px;
            display: block;
        }
        
        .file-upload-area:hover i { color: #4facfe; }
        
        .file-info {
            background: #e8f5e8;
            border: 1px solid #c3e6c3;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            display: none;
            align-items: center;
            gap: 10px;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 100%;
            justify-content: center;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .btn-info {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .btn-add {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 8px 16px;
            font-size: 0.9rem;
        }
        
        .hidden { display: none !important; }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        
        .summary-card.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .summary-card.green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .summary-card.purple { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        
        .summary-card h3 { font-size: 0.9rem; margin-bottom: 10px; opacity: 0.9; }
        .summary-card p { font-size: 1.5rem; font-weight: bold; }
        
        .split-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .split-panel {
            border: 1px solid #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            background: white;
        }
        
        .split-panel-header {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .split-panel-header h3 { font-size: 1.1rem; color: #495057; }
        
        .pedido-section {
            margin-bottom: 20px;
        }
        
        .pedido-header {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .pedido-header:hover { background: #e9ecef; }
        
        .pedido-header h3 { font-size: 1.1rem; color: #495057; }
        
        .badge {
            background: #17a2b8;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
        }
        
        .table-container {
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
            padding: 15px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        .data-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .data-table td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .data-table input {
            width: 100%;
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        
        .data-table tr:hover { background: #f8f9ff; }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        .action-buttons .btn { flex: 1; }
        
        .pdf-viewer {
            width: 100%;
            height: 600px;
            border: none;
        }
        
        .pedido-selector {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }
        
        .pedido-btn {
            padding: 8px 16px;
            background: #e9ecef;
            border: 2px solid transparent;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            color: #495057;
        }
        
        .pedido-btn:hover { background: #dee2e6; }
        
        .pedido-btn.active {
            background: #4facfe;
            color: white;
            border-color: #4facfe;
        }
        
        /* Melhorado estilo do menu contextual com z-index muito alto e estilos fortes */
        .context-menu {
            position: fixed !important;
            background: white !important;
            border: 2px solid #4facfe !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
            padding: 8px 0 !important;
            z-index: 999999 !important;
            display: none !important;
            min-width: 220px !important;
        }
        
        .context-menu.show {
            display: block !important;
        }
        
        .context-menu-item {
            padding: 14px 20px !important;
            cursor: pointer !important;
            transition: background 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            font-size: 0.95rem !important;
            color: #333 !important;
            background: white !important;
        }
        
        .context-menu-item:hover {
            background: #e3f2fd !important;
        }
        
        .context-menu-item i {
            width: 18px !important;
            color: #4facfe !important;
            font-size: 1rem !important;
        }
        
        /* Melhorado destaque para linha selecionada */
        .data-table tbody tr.selected {
            background: #e3f2fd !important;
            border-left: 4px solid #4facfe !important;
        }
        
        @media (max-width: 1200px) {
            .split-container {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .action-buttons { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-file-pdf"></i> Extrator de Pedidos PDF</h1>
            <p>Sistema para extrair informações de pedidos organizados por CNPJ</p>
        </header>

        <!-- Upload Section -->
        <div class="card upload-section" id="uploadSection">
            <div class="card-header">
                <h2><i class="fas fa-upload"></i> Upload do PDF</h2>
                <p>Faça upload do PDF para extrair pedidos por CNPJ e número</p>
            </div>
            <div class="card-content">
                <div class="file-upload-area" id="fileUploadArea">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Clique aqui ou arraste o arquivo PDF</p>
                    <input type="file" id="pdfFile" accept=".pdf" hidden>
                </div>
                
                <div class="file-info" id="fileInfo">
                    <i class="fas fa-file-pdf"></i>
                    <span id="fileName"></span>
                    <span id="fileSize"></span>
                </div>

                <button class="btn btn-primary" id="extractBtn" disabled>
                    <i class="fas fa-cogs"></i>
                    Extrair Informações
                </button>
            </div>
        </div>

        <!-- Processing Section -->
        <div class="card hidden" id="processingSection">
            <div class="card-header">
                <h2><i class="fas fa-cog fa-spin"></i> Processando</h2>
                <p>Extraindo dados do documento...</p>
            </div>
            <div class="card-content">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
        </div>

        <!-- Results Section -->
        <div class="card hidden" id="resultsSection">
            <div class="card-header">
                <h2><i class="fas fa-check-circle"></i> Dados Extraídos</h2>
            </div>
            <div class="card-content">
                <div class="summary-cards">
                    <div class="summary-card blue">
                        <h3>Total de CNPJs</h3>
                        <p id="totalCnpjs">0</p>
                    </div>
                    <div class="summary-card green">
                        <h3>Total de Pedidos</h3>
                        <p id="totalPedidos">0</p>
                    </div>
                    <div class="summary-card purple">
                        <h3>Total de Produtos</h3>
                        <p id="totalProdutos">0</p>
                    </div>
                </div>

                <div class="split-container">
                    <div class="split-panel">
                        <div class="split-panel-header">
                            <h3><i class="fas fa-table"></i> Dados Extraídos</h3>
                        </div>
                        <div id="pedidosContainer" style="max-height: 600px; overflow-y: auto;"></div>
                    </div>

                    <div class="split-panel">
                        <div class="split-panel-header">
                            <h3><i class="fas fa-file-pdf"></i> Visualizar PDF</h3>
                        </div>
                        <div style="padding: 15px;">
                            <div class="pedido-selector" id="pedidoSelector"></div>
                            <iframe class="pdf-viewer" id="pdfViewer"></iframe>
                        </div>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <button class="btn btn-warning" onclick="editarDados()">
                        <i class="fas fa-edit"></i>
                        Editar e Baixar Excel
                    </button>
                    <button class="btn btn-success" onclick="baixarDireto()">
                        <i class="fas fa-download"></i>
                        Baixar Excel Direto
                    </button>
                </div>
            </div>
        </div>

        <!-- Error Section -->
        <div class="card hidden" id="errorSection">
            <div class="card-header" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);">
                <h2><i class="fas fa-exclamation-triangle"></i> Erro</h2>
            </div>
            <div class="card-content" style="text-align: center;">
                <p id="errorMessage" style="color: #dc3545; margin-bottom: 20px;"></p>
                <button class="btn btn-info" onclick="resetForm()">
                    <i class="fas fa-redo"></i>
                    Tentar Novamente
                </button>
            </div>
        </div>
    </div>

    <!-- Menu contextual com estrutura simplificada -->
    <div class="context-menu" id="contextMenu">
        <div class="context-menu-item" id="addAbove">
            <i class="fas fa-arrow-up"></i>
            <span>Adicionar linha acima</span>
        </div>
        <div class="context-menu-item" id="addBelow">
            <i class="fas fa-arrow-down"></i>
            <span>Adicionar linha abaixo</span>
        </div>
    </div>

    <script>
        let sessionId = null;
        let extractedData = null;
        let isEditing = false;
        let currentPedido = null;
        let contextMenuRow = null;
        let contextMenuIndex = null;
        let contextMenuPIndex = null;

        const fileUploadArea = document.getElementById('fileUploadArea');
        const pdfFileInput = document.getElementById('pdfFile');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const extractBtn = document.getElementById('extractBtn');

        fileUploadArea.addEventListener('click', () => pdfFileInput.click());
        fileUploadArea.addEventListener('dragover', handleDragOver);
        fileUploadArea.addEventListener('drop', handleDrop);
        pdfFileInput.addEventListener('change', handleFileSelect);
        extractBtn.addEventListener('click', extractPDF);

        function handleDragOver(e) {
            e.preventDefault();
            fileUploadArea.style.borderColor = '#4facfe';
            fileUploadArea.style.backgroundColor = '#f8f9ff';
        }

        function handleDrop(e) {
            e.preventDefault();
            fileUploadArea.style.borderColor = '#ddd';
            fileUploadArea.style.backgroundColor = 'transparent';
            const files = e.dataTransfer.files;
            if (files.length > 0) handleFile(files[0]);
        }

        function handleFileSelect(e) {
            const file = e.target.files[0];
            if (file) handleFile(file);
        }

        function handleFile(file) {
            if (file.type !== 'application/pdf') {
                showError('Por favor, selecione um arquivo PDF válido.');
                return;
            }
            fileName.textContent = file.name;
            fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            fileInfo.style.display = 'flex';
            extractBtn.disabled = false;
            hideAllSections();
        }

        function hideAllSections() {
            document.getElementById('processingSection').classList.add('hidden');
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('errorSection').classList.add('hidden');
        }

        function showError(message) {
            hideAllSections();
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorSection').classList.remove('hidden');
        }

        function resetForm() {
            pdfFileInput.value = '';
            fileInfo.style.display = 'none';
            extractBtn.disabled = true;
            sessionId = null;
            extractedData = null;
            isEditing = false;
            currentPedido = null;
            hideAllSections();
        }

        async function extractPDF() {
            const file = pdfFileInput.files[0];
            if (!file) {
                showError('Por favor, selecione um arquivo PDF.');
                return;
            }

            hideAllSections();
            document.getElementById('processingSection').classList.remove('hidden');
            simulateProgress();

            try {
                const formData = new FormData();
                formData.append('pdf', file);

                const response = await fetch('/api/extract-pdf', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Erro ao processar PDF');
                }

                const data = await response.json();
                sessionId = data.session_id;
                extractedData = data;
                
                showResults(data);
                createPedidoSelector(data.dados);
                if (data.dados.length > 0) {
                    loadPDFByOrder(data.dados[0].pedido);
                }
            } catch (error) {
                console.error('Erro na extração:', error);
                showError(error.message || 'Erro ao extrair informações do PDF.');
            }
        }

        function simulateProgress() {
            let progress = 0;
            const progressFill = document.getElementById('progressFill');
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 100) progress = 100;
                progressFill.style.width = progress + '%';
                if (progress >= 100) clearInterval(interval);
            }, 200);
        }

        function showResults(data) {
            hideAllSections();
            document.getElementById('resultsSection').classList.remove('hidden');

            document.getElementById('totalCnpjs').textContent = data.total_cnpjs;
            document.getElementById('totalPedidos').textContent = data.dados.length;
            
            let totalProdutos = 0;
            data.dados.forEach(item => totalProdutos += item.total_produtos);
            document.getElementById('totalProdutos').textContent = totalProdutos;

            renderPedidos(data.dados);
        }

        function createPedidoSelector(dados) {
            const selector = document.getElementById('pedidoSelector');
            selector.innerHTML = '';

            dados.forEach((item, index) => {
                const btn = document.createElement('button');
                btn.className = 'pedido-btn' + (index === 0 ? ' active' : '');
                btn.textContent = `Pedido ${item.pedido}`;
                btn.onclick = () => {
                    document.querySelectorAll('.pedido-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    loadPDFByOrder(item.pedido);
                    scrollToPedido(index);
                };
                selector.appendChild(btn);
            });
        }

        function scrollToPedido(index) {
            const sections = document.querySelectorAll('.pedido-section');
            if (sections[index]) {
                sections[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        async function loadPDFByOrder(pedido) {
            currentPedido = pedido;
            try {
                const response = await fetch('/api/get-pdf-by-order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        session_id: sessionId,
                        pedido: pedido
                    })
                });

                if (!response.ok) throw new Error('Erro ao carregar PDF');

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                document.getElementById('pdfViewer').src = url;
            } catch (error) {
                console.error('Erro ao carregar PDF:', error);
            }
        }

        function renderPedidos(dados) {
            const container = document.getElementById('pedidosContainer');
            container.innerHTML = '';

            dados.forEach((item, index) => {
                const section = document.createElement('div');
                section.className = 'pedido-section';
                section.id = `pedido-section-${index}`;
                
                const header = document.createElement('div');
                header.className = 'pedido-header';
                header.innerHTML = `
                    <h3><i class="fas fa-receipt"></i> CNPJ: ${item.cnpj} | Pedido: ${item.pedido}</h3>
                    <span class="badge">${item.total_produtos} produtos</span>
                `;
                header.onclick = () => {
                    const pedidoBtns = document.querySelectorAll('.pedido-btn');
                    pedidoBtns.forEach(b => b.classList.remove('active'));
                    if (pedidoBtns[index]) {
                        pedidoBtns[index].classList.add('active');
                    }
                    loadPDFByOrder(item.pedido);
                };
                
                const tableContainer = document.createElement('div');
                tableContainer.className = 'table-container';
                
                const table = document.createElement('table');
                table.className = 'data-table';
                table.id = `table-${index}`;
                table.innerHTML = `
                    <thead>
                        <tr>
                            <th>SKU</th>
                            <th>Descrição</th>
                            <th>Quantidade</th>
                            <th>Valor Unitário</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${item.produtos.map((produto, pIndex) => `
                            <tr data-index="${index}" data-pindex="${pIndex}">
                                <td>
                                    <input type="text" 
                                           value="${produto.SKU}" 
                                           data-index="${index}" 
                                           data-pindex="${pIndex}" 
                                           data-field="SKU"
                                           ${isEditing ? '' : 'readonly'}>
                                </td>
                                <td>
                                    <input type="text" 
                                           value="${produto.Descricao}" 
                                           data-index="${index}" 
                                           data-pindex="${pIndex}" 
                                           data-field="Descricao"
                                           ${isEditing ? '' : 'readonly'}>
                                </td>
                                <td>
                                    <input type="text" 
                                           value="${produto.Quantidade}" 
                                           data-index="${index}" 
                                           data-pindex="${pIndex}" 
                                           data-field="Quantidade"
                                           ${isEditing ? '' : 'readonly'}>
                                </td>
                                <td>
                                    <input type="text" 
                                           value="${produto.Valor_Unitario}" 
                                           data-index="${index}" 
                                           data-pindex="${pIndex}" 
                                           data-field="Valor_Unitario"
                                           ${isEditing ? '' : 'readonly'}>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                `;
                
                tableContainer.appendChild(table);
                section.appendChild(header);
                section.appendChild(tableContainer);
                container.appendChild(section);
            });

            document.querySelectorAll('.data-table tbody tr').forEach(row => {
                row.addEventListener('contextmenu', handleContextMenu);
            });

            if (isEditing) {
                document.querySelectorAll('.data-table input').forEach(input => {
                    input.addEventListener('change', handleDataChange);
                });
            }
        }

        function handleContextMenu(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('[v0] Menu contextual acionado');
            
            const row = e.currentTarget;
            contextMenuRow = row;
            contextMenuIndex = parseInt(row.dataset.index);
            contextMenuPIndex = parseInt(row.dataset.pindex);
            
            console.log('[v0] Linha selecionada - Index:', contextMenuIndex, 'PIndex:', contextMenuPIndex);
            
            // Remover seleção anterior
            document.querySelectorAll('.data-table tbody tr').forEach(r => r.classList.remove('selected'));
            row.classList.add('selected');
            
            // Mostrar menu
            const contextMenu = document.getElementById('contextMenu');
            contextMenu.classList.add('show');
            contextMenu.style.display = 'block';
            
            // Posicionar menu
            const x = e.pageX;
            const y = e.pageY;
            contextMenu.style.left = x + 'px';
            contextMenu.style.top = y + 'px';
            
            console.log('[v0] Menu posicionado em:', x, y);
            console.log('[v0] Menu display:', contextMenu.style.display);
            console.log('[v0] Menu classes:', contextMenu.className);
        }

        document.addEventListener('click', (e) => {
            const contextMenu = document.getElementById('contextMenu');
            if (!contextMenu.contains(e.target)) {
                contextMenu.classList.remove('show');
                contextMenu.style.display = 'none';
                document.querySelectorAll('.data-table tbody tr').forEach(r => r.classList.remove('selected'));
            }
        });

        document.getElementById('addAbove').addEventListener('click', (e) => {
            e.stopPropagation();
            console.log('[v0] Adicionar linha acima clicado');
            const contextMenu = document.getElementById('contextMenu');
            contextMenu.classList.remove('show');
            contextMenu.style.display = 'none';
            adicionarLinhaAcima();
        });

        document.getElementById('addBelow').addEventListener('click', (e) => {
            e.stopPropagation();
            console.log('[v0] Adicionar linha abaixo clicado');
            const contextMenu = document.getElementById('contextMenu');
            contextMenu.classList.remove('show');
            contextMenu.style.display = 'none';
            adicionarLinhaAbaixo();
        });

        async function adicionarLinhaAcima() {
            console.log('[v0] Função adicionarLinhaAcima chamada');
            console.log('[v0] contextMenuIndex:', contextMenuIndex, 'contextMenuPIndex:', contextMenuPIndex);
            
            if (contextMenuIndex === null || contextMenuPIndex === null) {
                console.log('[v0] Índices não definidos, abortando');
                return;
            }
            
            const item = extractedData.dados[contextMenuIndex];
            console.log('[v0] Item selecionado:', item);
            
            document.getElementById('contextMenu').style.display = 'none';
            
            try {
                const response = await fetch('/api/add-product', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId,
                        cnpj: item.cnpj,
                        pedido: item.pedido
                    })
                });

                if (!response.ok) throw new Error('Erro ao adicionar linha');

                const result = await response.json();
                console.log('[v0] Produto adicionado:', result.produto);
                
                extractedData.dados[contextMenuIndex].produtos.splice(contextMenuPIndex, 0, result.produto);
                extractedData.dados[contextMenuIndex].total_produtos++;
                
                let totalProdutos = 0;
                extractedData.dados.forEach(item => totalProdutos += item.total_produtos);
                document.getElementById('totalProdutos').textContent = totalProdutos;
                
                renderPedidos(extractedData.dados);
                
                if (isEditing) {
                    document.querySelectorAll('.data-table input').forEach(input => {
                        input.addEventListener('change', handleDataChange);
                    });
                }
                
                console.log('[v0] Linha adicionada com sucesso acima');
            } catch (error) {
                console.error('[v0] Erro ao adicionar linha:', error);
                showError('Erro ao adicionar linha: ' + error.message);
            }
        }

        async function adicionarLinhaAbaixo() {
            console.log('[v0] Função adicionarLinhaAbaixo chamada');
            console.log('[v0] contextMenuIndex:', contextMenuIndex, 'contextMenuPIndex:', contextMenuPIndex);
            
            if (contextMenuIndex === null || contextMenuPIndex === null) {
                console.log('[v0] Índices não definidos, abortando');
                return;
            }
            
            const item = extractedData.dados[contextMenuIndex];
            console.log('[v0] Item selecionado:', item);
            
            document.getElementById('contextMenu').style.display = 'none';
            
            try {
                const response = await fetch('/api/add-product', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId,
                        cnpj: item.cnpj,
                        pedido: item.pedido
                    })
                });

                if (!response.ok) throw new Error('Erro ao adicionar linha');

                const result = await response.json();
                console.log('[v0] Produto adicionado:', result.produto);
                
                extractedData.dados[contextMenuIndex].produtos.splice(contextMenuPIndex + 1, 0, result.produto);
                extractedData.dados[contextMenuIndex].total_produtos++;
                
                let totalProdutos = 0;
                extractedData.dados.forEach(item => totalProdutos += item.total_produtos);
                document.getElementById('totalProdutos').textContent = totalProdutos;
                
                renderPedidos(extractedData.dados);
                
                if (isEditing) {
                    document.querySelectorAll('.data-table input').forEach(input => {
                        input.addEventListener('change', handleDataChange);
                    });
                }
                
                console.log('[v0] Linha adicionada com sucesso abaixo');
            } catch (error) {
                console.error('[v0] Erro ao adicionar linha:', error);
                showError('Erro ao adicionar linha: ' + error.message);
            }
        }

        function handleDataChange(e) {
            const index = parseInt(e.target.dataset.index);
            const pIndex = parseInt(e.target.dataset.pindex);
            const field = e.target.dataset.field;
            const value = e.target.value;

            extractedData.dados[index].produtos[pIndex][field] = value;
        }

        function editarDados() {
            isEditing = true;
            renderPedidos(extractedData.dados);
            
            const editBtn = document.querySelector('.btn-warning');
            editBtn.innerHTML = '<i class="fas fa-save"></i> Salvar e Baixar Excel';
            editBtn.onclick = salvarEBaixar;
        }

        async function salvarEBaixar() {
            try {
                await fetch('/api/update-data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId,
                        dados: extractedData.dados
                    })
                });

                await baixarExcel();
            } catch (error) {
                showError('Erro ao salvar dados: ' + error.message);
            }
        }

        async function baixarDireto() {
            await baixarExcel();
        }

        async function baixarExcel() {
            try {
                const response = await fetch('/api/generate-excel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId })
                });

                if (!response.ok) throw new Error('Erro ao gerar Excel');

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'produtos_por_cnpj_pedido.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (error) {
                showError('Erro ao baixar Excel: ' + error.message);
            }
        }
    </script>
</body>
</html>
    '''
