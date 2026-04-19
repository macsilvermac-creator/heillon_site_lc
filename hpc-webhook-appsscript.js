// ═══════════════════════════════════════════════════════════════
// HEILLON HPC — Apps Script Webhook para Google Sheets
// ═══════════════════════════════════════════════════════════════
//
// COMO INSTALAR (uma vez, 5 minutos):
//
// 1. Abrir o Google Sheet: https://docs.google.com/spreadsheets/d/1bjFVqT4FM9qGEmthKRluiYRMufcLfAjn3MXEsgSmK-s
// 2. Menu: Extensões → Apps Script
// 3. Apagar o código existente e colar este ficheiro completo
// 4. Salvar (Ctrl+S)
// 5. Clique em "Implementar" → "Nova implementação"
// 6. Tipo: "Aplicativo da Web"
// 7. Executar como: "Eu"
// 8. Quem tem acesso: "Qualquer pessoa"
// 9. Implementar → Copiar o URL gerado
// 10. No ficheiro hpc-gate.html, substituir PLACEHOLDER_APPS_SCRIPT_URL pelo URL copiado
// 11. Commitar e fazer push
// ═══════════════════════════════════════════════════════════════

var SHEET_ID   = '1bjFVqT4FM9qGEmthKRluiYRMufcLfAjn3MXEsgSmK-s';
var SHEET_NAME = 'Leads';

// Cabeçalhos da tabela
var HEADERS = [
  'Data/Hora', 'Nome', 'Email', 'Telefone', 'Cidade', 'Estado',
  'Plano', 'Opt-in', 'Origem', 'Timezone', 'Idioma', 'User-Agent'
];

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss    = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    // Criar cabeçalhos se a sheet estiver vazia
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.getRange(1, 1, 1, HEADERS.length)
           .setFontWeight('bold')
           .setBackground('#1a1a2e')
           .setFontColor('#C9A84C');
      sheet.setFrozenRows(1);
    }

    // Formatar data/hora em PT-BR
    var ts = data.ts ? new Date(data.ts) : new Date();
    var tsFormatted = Utilities.formatDate(ts, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm:ss');

    // Inserir linha
    sheet.appendRow([
      tsFormatted,
      data.nome     || '',
      data.email    || '',
      data.telefone || '',
      data.cidade   || '',
      data.estado   || '',
      data.plano    || 'observacao',
      data.optin    ? 'Sim' : 'Não',
      data.origem   || '',
      data.tz       || '',
      data.lang     || '',
      data.ua       || ''
    ]);

    // Colorir plano
    var lastRow = sheet.getLastRow();
    var plano   = (data.plano || '').toLowerCase();
    var bgColor = '#0d1520'; // default
    if (plano === 'sovereign')   bgColor = '#1a1400';
    if (plano === 'council')     bgColor = '#0a1520';
    if (plano === 'enterprise')  bgColor = '#120d1a';
    sheet.getRange(lastRow, 1, 1, HEADERS.length).setBackground(bgColor);

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
                         .setMimeType(ContentService.MimeType.JSON);

  } catch(err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: err.message }))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}

// GET para teste (abre no browser para verificar se está a funcionar)
function doGet(e) {
  var ss    = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);
  var count = sheet ? Math.max(0, sheet.getLastRow() - 1) : 0;
  return ContentService.createTextOutput(
    JSON.stringify({ ok: true, message: 'HEILLON HPC Webhook activo', leads: count })
  ).setMimeType(ContentService.MimeType.JSON);
}
