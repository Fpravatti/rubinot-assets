// generate-index.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TILES_DIR = __dirname;
const OUTPUT_FILE = path.join(__dirname, '..', 'map-index.json');

console.log(`📂 Lendo arquivos de: ${TILES_DIR}`);

try {
  const files = fs.readdirSync(TILES_DIR);

  const tiles = files
    .filter(file => file.startsWith('Minimap_Color_') && file.endsWith('.png'))
    .map(file =>
      file.replace('Minimap_Color_', '').replace('.png', '')
    );

  const jsonOutput = {
    tiles,
    count: tiles.length
  };

  fs.writeFileSync(
    OUTPUT_FILE,
    JSON.stringify(jsonOutput, null, 2),
    'utf-8'
  );

  console.log(`✅ Sucesso! Índice gerado com ${tiles.length} tiles.`);
  console.log(`📄 Salvo em: ${OUTPUT_FILE}`);

} catch (error) {
  console.error("❌ Erro ao gerar o índice do mapa.");
  console.error(error);
}
