let extractedData = null
let sessionId = null
let contextMenuRow = null
let contextMenuPedidoIndex = null
let isEditing = false

// Elementos DOM
const fileUploadArea = document.getElementById("fileUploadArea")
const pdfFileInput = document.getElementById("pdfFile")
const fileInfo = document.getElementById("fileInfo")
const fileName = document.getElementById("fileName")
const fileSize = document.getElementById("fileSize")
const extractBtn = document.getElementById("extractBtn")
const statusSection = document.getElementById("statusSection")
const resultsSection = document.getElementById("resultsSection")
const errorSection = document.getElementById("errorSection")
const progressFill = document.getElementById("progressFill")
const editBtn = document.getElementById("editBtn")
const downloadBtn = document.getElementById("downloadBtn")
const dataPanel = document.getElementById("dataPanel")
const contextMenu = document.getElementById("contextMenu")
const pedidoSelector = document.getElementById("pedidoSelector")
const pdfViewer = document.querySelector(".pdf-viewer")

// Event listeners
fileUploadArea.addEventListener("click", () => pdfFileInput.click())
fileUploadArea.addEventListener("dragover", handleDragOver)
fileUploadArea.addEventListener("drop", handleDrop)
pdfFileInput.addEventListener("change", handleFileSelect)
extractBtn.addEventListener("click", extractPDF)
editBtn.addEventListener("click", editarDados)
downloadBtn.addEventListener("click", baixarDireto)

pedidoSelector.addEventListener("change", carregarPDFPorPedido)

document.querySelectorAll(".context-menu-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault()
    e.stopPropagation()

    const action = this.dataset.action
    console.log("[v0] Menu item clicado:", action)

    contextMenu.classList.remove("show")

    if (contextMenuRow !== null && contextMenuPedidoIndex !== null) {
      if (action === "delete") {
        excluirLinha(contextMenuRow, contextMenuPedidoIndex)
      } else {
        adicionarLinha(action, contextMenuRow, contextMenuPedidoIndex)
      }
    }
  })
})

// Fechar menu contextual ao clicar fora
document.addEventListener("click", () => {
  contextMenu.classList.remove("show")
})

// Prevenir fechamento ao clicar no menu
contextMenu.addEventListener("click", (e) => {
  e.stopPropagation()
})

function handleDragOver(e) {
  e.preventDefault()
  fileUploadArea.style.borderColor = "#4facfe"
  fileUploadArea.style.backgroundColor = "#f8f9ff"
}

function handleDrop(e) {
  e.preventDefault()
  fileUploadArea.style.borderColor = "#ddd"
  fileUploadArea.style.backgroundColor = "transparent"

  const files = e.dataTransfer.files
  if (files.length > 0) {
    handleFile(files[0])
  }
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    handleFile(file)
  }
}

function handleFile(file) {
  if (file.type !== "application/pdf") {
    showError("Por favor, selecione um arquivo PDF válido.")
    return
  }

  fileName.textContent = file.name
  fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`
  fileInfo.style.display = "flex"
  extractBtn.disabled = false

  hideAllSections()
}

function hideAllSections() {
  statusSection.classList.add("hidden")
  resultsSection.classList.add("hidden")
  errorSection.classList.add("hidden")
}

function showError(message) {
  hideAllSections()
  document.getElementById("errorMessage").textContent = message
  errorSection.classList.remove("hidden")
}

function resetForm() {
  pdfFileInput.value = ""
  fileInfo.style.display = "none"
  extractBtn.disabled = true
  extractedData = null
  sessionId = null
  isEditing = false
  hideAllSections()
}

async function extractPDF() {
  const file = pdfFileInput.files[0]
  if (!file) {
    showError("Por favor, selecione um arquivo PDF.")
    return
  }

  hideAllSections()
  statusSection.classList.remove("hidden")
  simulateProgress()

  try {
    const formData = new FormData()
    formData.append("pdf", file)

    const response = await fetch("/api/extract-pdf", {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || "Erro ao processar PDF")
    }

    const data = await response.json()
    extractedData = data
    sessionId = data.session_id

    showResults()
  } catch (error) {
    console.error("Erro na extração:", error)
    showError(error.message || "Erro ao extrair informações do PDF.")
  }
}

function simulateProgress() {
  let progress = 0
  const interval = setInterval(() => {
    progress += Math.random() * 10 + 5
    if (progress > 100) progress = 100

    progressFill.style.width = progress + "%"

    if (progress >= 100) {
      clearInterval(interval)
    }
  }, 200)
}

function showResults() {
  hideAllSections()
  resultsSection.classList.remove("hidden")

  // Limpar painel
  dataPanel.innerHTML = ""

  pedidoSelector.innerHTML = '<option value="">Selecione um pedido</option>'

  // Renderizar dados
  extractedData.dados.forEach((item, index) => {
    const option = document.createElement("option")
    option.value = index
    option.textContent = `CNPJ: ${item.cnpj} - Pedido: ${item.pedido}`
    pedidoSelector.appendChild(option)

    // Criar seção de pedido
    const section = document.createElement("div")
    section.className = "order-section"
    section.dataset.index = index
    section.id = `pedido-section-${index}` // Adicionar ID para scroll

    const header = document.createElement("div")
    header.className = "order-header"
    header.innerHTML = `
            <i class="fas fa-receipt"></i> 
            CNPJ: ${item.cnpj} - Pedido: ${item.pedido}
            <span style="margin-left: 10px; font-size: 0.9rem; opacity: 0.8;">
                (${item.total_produtos} produtos)
            </span>
        `

    header.addEventListener("click", () => {
      sincronizarPedido(index)
    })

    const tableContainer = document.createElement("div")
    tableContainer.className = "table-container"

    const table = document.createElement("table")
    table.className = "data-table"
    table.innerHTML = `
            <thead>
                <tr>
                    <th>SKU</th>
                    <th>Descrição</th>
                    <th>Quantidade</th>
                    <th>Valor Unitário</th>
                </tr>
            </thead>
            <tbody></tbody>
        `

    const tbody = table.querySelector("tbody")

    item.produtos.forEach((produto, prodIndex) => {
      const row = document.createElement("tr")
      row.dataset.pedidoIndex = index
      row.dataset.produtoIndex = prodIndex

      row.innerHTML = `
                <td><input type="text" value="${produto.SKU || ""}" data-field="SKU" ${isEditing ? "" : "readonly"}></td>
                <td><input type="text" value="${produto.Descricao || ""}" data-field="Descricao" ${isEditing ? "" : "readonly"}></td>
                <td><input type="text" value="${produto.Quantidade || ""}" data-field="Quantidade" ${isEditing ? "" : "readonly"}></td>
                <td><input type="text" value="${produto.Valor_Unitario || ""}" data-field="Valor_Unitario" ${isEditing ? "" : "readonly"}></td>
            `

      row.addEventListener("contextmenu", (e) => {
        e.preventDefault()
        e.stopPropagation()

        console.log("[v0] Botão direito clicado - Linha:", prodIndex, "Pedido:", index)

        contextMenuRow = prodIndex
        contextMenuPedidoIndex = index

        // Remover seleção anterior
        document.querySelectorAll(".data-table tbody tr").forEach((r) => r.classList.remove("selected"))
        row.classList.add("selected")

        const x = e.clientX
        const y = e.clientY

        // Garantir que o menu não saia da tela
        const menuWidth = 200
        const menuHeight = 120 // Aumentado para acomodar 3 itens
        const windowWidth = window.innerWidth
        const windowHeight = window.innerHeight

        let finalX = x
        let finalY = y

        if (x + menuWidth > windowWidth) {
          finalX = windowWidth - menuWidth - 10
        }

        if (y + menuHeight > windowHeight) {
          finalY = windowHeight - menuHeight - 10
        }

        contextMenu.style.left = finalX + "px"
        contextMenu.style.top = finalY + "px"
        contextMenu.classList.add("show")

        console.log("[v0] Menu contextual exibido em:", finalX, finalY)
      })

      tbody.appendChild(row)
    })

    tableContainer.appendChild(table)
    section.appendChild(header)
    section.appendChild(tableContainer)
    dataPanel.appendChild(section)
  })

  if (isEditing) {
    adicionarEventListenersEdicao()
  }
}

function sincronizarPedido(index) {
  console.log("[v0] Sincronizando pedido:", index)

  // Atualizar seletor
  pedidoSelector.value = index

  document.querySelectorAll(".order-section").forEach((section) => {
    section.classList.remove("active-section")
  })

  // Destacar seção ativa
  const activeSection = document.getElementById(`pedido-section-${index}`)
  if (activeSection) {
    activeSection.classList.add("active-section")
  }

  // Carregar PDF correspondente
  carregarPDFPorPedido()
}

async function carregarPDFPorPedido() {
  const selectedIndex = pedidoSelector.value

  if (!selectedIndex || selectedIndex === "") {
    pdfViewer.innerHTML = `
      <div class="pdf-placeholder">
        <i class="fas fa-file-pdf" style="font-size: 3rem; margin-bottom: 15px; display: block; color: #ddd;"></i>
        Selecione um pedido para visualizar o PDF
      </div>
    `
    document.querySelectorAll(".order-section").forEach((section) => {
      section.classList.remove("active-section")
    })
    return
  }

  document.querySelectorAll(".order-section").forEach((section) => {
    section.classList.remove("active-section")
  })
  const activeSection = document.getElementById(`pedido-section-${selectedIndex}`)
  if (activeSection) {
    activeSection.classList.add("active-section")
    // Scroll suave para a seção
    activeSection.scrollIntoView({ behavior: "smooth", block: "start" })
  }

  const pedidoData = extractedData.dados[selectedIndex]

  try {
    pdfViewer.innerHTML = '<div class="pdf-placeholder">Carregando PDF...</div>'

    const response = await fetch(`/api/get-pdf-by-order?session_id=${sessionId}&pedido=${pedidoData.pedido}`, {
      method: "GET",
    })

    if (!response.ok) {
      throw new Error("Erro ao carregar PDF")
    }

    const blob = await response.blob()
    const url = URL.createObjectURL(blob)

    pdfViewer.innerHTML = `<iframe src="${url}" width="100%" height="700px" style="border: none; border-radius: 8px;"></iframe>`

    console.log("[v0] PDF carregado para pedido:", pedidoData.pedido)
  } catch (error) {
    console.error("[v0] Erro ao carregar PDF:", error)
    pdfViewer.innerHTML = `
      <div class="pdf-placeholder" style="color: #dc3545;">
        <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 15px; display: block;"></i>
        Erro ao carregar PDF: ${error.message}
      </div>
    `
  }
}

function editarDados() {
  isEditing = true

  // Remover readonly de todos os inputs
  document.querySelectorAll(".data-table input").forEach((input) => {
    input.removeAttribute("readonly")
  })

  // Adicionar event listeners para capturar mudanças
  adicionarEventListenersEdicao()

  // Alterar botão para "Salvar e Baixar"
  editBtn.innerHTML = '<i class="fas fa-save"></i> Salvar e Baixar Excel'
  editBtn.onclick = salvarEBaixar

  console.log("[v0] Modo de edição ativado")
}

function adicionarEventListenersEdicao() {
  document.querySelectorAll(".data-table input").forEach((input) => {
    input.addEventListener("change", handleDataChange)
  })
}

function handleDataChange(e) {
  const input = e.target
  const row = input.closest("tr")
  const pedidoIndex = Number.parseInt(row.dataset.pedidoIndex)
  const produtoIndex = Number.parseInt(row.dataset.produtoIndex)
  const field = input.dataset.field
  const value = input.value

  // Atualizar dados no extractedData
  extractedData.dados[pedidoIndex].produtos[produtoIndex][field] = value

  console.log("[v0] Dado atualizado:", field, "=", value)
}

async function salvarEBaixar() {
  try {
    console.log("[v0] Salvando dados editados...")

    // Enviar dados atualizados para o backend
    const response = await fetch("/api/update-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        dados: extractedData.dados,
      }),
    })

    if (!response.ok) {
      throw new Error("Erro ao salvar dados")
    }

    console.log("[v0] Dados salvos com sucesso")

    // Baixar Excel com dados atualizados
    await baixarExcel()

    isEditing = false
    editBtn.innerHTML = '<i class="fas fa-edit"></i> Editar e Baixar Excel'
    editBtn.onclick = editarDados

    // Remover destaque dos inputs
    document.querySelectorAll(".data-table input").forEach((input) => {
      input.setAttribute("readonly", true)
    })
  } catch (error) {
    console.error("[v0] Erro ao salvar e baixar:", error)
    showError("Erro ao salvar dados: " + error.message)
  }
}

async function baixarDireto() {
  await baixarExcel()
}

async function baixarExcel() {
  if (!sessionId) {
    showError("Nenhum dado para download.")
    return
  }

  try {
    const response = await fetch("/api/generate-excel", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
      }),
    })

    if (!response.ok) {
      throw new Error("Erro ao gerar arquivo Excel")
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.style.display = "none"
    a.href = url
    a.download = `produtos_por_cnpj_pedido.xlsx`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)

    // Feedback visual
    const originalHTML = downloadBtn.innerHTML
    downloadBtn.innerHTML = '<i class="fas fa-check"></i> Excel Baixado!'
    setTimeout(() => {
      downloadBtn.innerHTML = originalHTML
    }, 3000)

    console.log("[v0] Excel baixado com sucesso")
  } catch (error) {
    console.error("[v0] Erro no download:", error)
    showError("Erro ao baixar arquivo Excel.")
  }
}

async function adicionarLinha(position, rowIndex, pedidoIndex) {
  console.log("[v0] Adicionando linha", position, "na posição", rowIndex, "do pedido", pedidoIndex)

  try {
    const pedidoData = extractedData.dados[pedidoIndex]

    const response = await fetch("/api/add-product", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        cnpj: pedidoData.cnpj,
        pedido: pedidoData.pedido,
        index: rowIndex,
        position: position,
      }),
    })

    if (!response.ok) {
      throw new Error("Erro ao adicionar produto")
    }

    const result = await response.json()
    console.log("[v0] Produto adicionado com sucesso", result)

    const insertIndex = position === "above" ? rowIndex : rowIndex + 1
    extractedData.dados[pedidoIndex].produtos.splice(insertIndex, 0, result.produto)
    extractedData.dados[pedidoIndex].total_produtos++

    // Atualizar visualização
    showResults()
  } catch (error) {
    console.error("[v0] Erro ao adicionar linha:", error)
    showError("Erro ao adicionar linha: " + error.message)
  }
}

async function excluirLinha(rowIndex, pedidoIndex) {
  console.log("[v0] Excluindo linha", rowIndex, "do pedido", pedidoIndex)

  // Confirmar exclusão
  if (!confirm("Tem certeza que deseja excluir esta linha?")) {
    return
  }

  try {
    const pedidoData = extractedData.dados[pedidoIndex]

    const response = await fetch("/api/delete-product", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        cnpj: pedidoData.cnpj,
        pedido: pedidoData.pedido,
        index: rowIndex,
      }),
    })

    if (!response.ok) {
      throw new Error("Erro ao excluir produto")
    }

    const result = await response.json()
    console.log("[v0] Produto excluído com sucesso", result)

    // Remover do array local
    extractedData.dados[pedidoIndex].produtos.splice(rowIndex, 1)
    extractedData.dados[pedidoIndex].total_produtos--

    // Atualizar visualização
    showResults()
  } catch (error) {
    console.error("[v0] Erro ao excluir linha:", error)
    showError("Erro ao excluir linha: " + error.message)
  }
}
