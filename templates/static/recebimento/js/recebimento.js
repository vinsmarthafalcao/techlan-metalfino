import { QRCodeModal } from '../../geral/js/modals.js';
import { PackageGrid } from '../../geral/js/packageGrid.js';
import { setMessage, clearMessage, ajaxRequest, isLoading } from '../../geral/js/utils.js';

function ReceiptGrid(){
    this.btReadPackage = document.getElementById('lerEmbalagem')
    this.btSummarize = document.getElementById('sumarizar')
    this.lbMessage = document.getElementById('msg')
    this.loading = document.getElementById('recebimentoLoading')
    this.URL = document.body.dataset.url
    this.packageGrid = new PackageGrid()
    this.qrCodeModal = new QRCodeModal(this.packageGrid.packagesExists, this.packageGrid.getPackage)

    this.btReadPackage.addEventListener('click', this.qrCodeModal.open)
    this.btSummarize.addEventListener('click', () => {
        clearMessage(this.lbMessage)
        if (this.packageGrid.packages.length === 0) setMessage('Nenhuma embalagem foi lida!', 'error', this.lbMessage)
        else this.receiptModal.open(this.packageGrid.packages, this.packageGrid.deposito.coddep)
    })

    // Envio para transferência de estoque
    this.toReceive = async depositDestination => {
        clearMessage(this.lbMessage)
        isLoading(this.loading, true)
        this.receiptModal.close()
        if (this.packageGrid.packages.length === 0) setMessage('Nada a transferir!', 'error', this.lbMessage)
        const request = {
            origem: this.packageGrid.deposito.coddep,
            destino: depositDestination,
            embalagens: this.packageGrid.packages.map(packageItem => packageItem ? {numemb:packageItem.numemb, veremb:packageItem.veremb}: null)
        }
        const response = await ajaxRequest(this.URL, request)
        if (response.ok) {
            this.packageGrid.packages.forEach(packageItem=> {
                packageItem.deposito.coddep = response.coddep
                packageItem.deposito.desdep = response.desdep
                packageItem.updatePackage()
            })
            this.packageGrid.deposito.coddep = response.coddep
            this.packageGrid.deposito.desdep = response.desdep
            setMessage(response.message, 'success', this.lbMessage)
        }
        else setMessage(response.message, 'error', this.lbMessage)
        isLoading(this.loading, false)
    }
    this.receiptModal = new ReceiptModal(this.toReceive)
        
}

function ReceiptModal(toReceive) {
    this.transferList = []
    this.table = document.querySelector("#modal-sumarizar")
    this.tableBody = this.table.querySelector("tbody")
    this.btReceive = this.table.querySelector('#btreceive')
    this.btClose = this.table.querySelector('#btclose')
    this.depositDestination = this.table.querySelector('#depositDestination')

    // sumariza embalagens
    this.summarize = packages => {
        const summary = {}
        packages.forEach(packageItem => {
            const key = `${packageItem.codpro}-${packageItem.history.codori}-${packageItem.history.numorp}-${packageItem.codlot}`
            if(!summary[key]) 
                summary[key] = { produto: packageItem.codpro, OP: packageItem.history.codori+'-'+packageItem.history.numorp, lote: packageItem.codlot  , quantidade: packageItem.qtdemb }
            else summary[key].quantidade += packageItem.qtdemb
        })
        this.transferList = Object.values(summary)
    }

    // Rendenriza lista de transferência
    this.renderList = () => {
        this.tableBody.innerHTML = ""; 
        this.transferList.forEach(item => {
            const row = document.createElement("tr");
            row.classList.add("border-b");
            row.innerHTML = `
                <td class="py-2">${item.produto}</td>
                <td class="py-2">${item.OP}</td>
                <td class="py-2">${item.lote}</td>
                <td class="py-2 text-center">${item.quantidade}</td>`
    
            this.tableBody.appendChild(row)
        });
    }

    // Busca depósito de destino
    this.getDepositDestination = async deposit => {
        let depositDestination = await ajaxRequest(this.depositDestination.dataset.url, deposit)
        this.depositDestination.value = depositDestination.desdep
        this.depositDestination.dataset.coddep = depositDestination.coddep
    }

    // Abrir modal
    this.open = async (packages, deposit) => {
        await this.getDepositDestination(deposit)
        this.table.classList.remove('hidden')
        this.summarize(packages)
        this.renderList()
    }

    // Fecha modal
    this.close = () => {
        this.transferList.length = 0
        this.tableBody.innerHTML = ''
        this.table.classList.add('hidden')
    }

    this.btClose.addEventListener('click', this.close)
    this.btReceive.addEventListener('click', () => toReceive(this.depositDestination.dataset.coddep))
}

document.addEventListener('DOMContentLoaded', () => {
    new ReceiptGrid()
})