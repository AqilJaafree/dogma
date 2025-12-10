/**
 * Simple script to generate PWA icons using Canvas
 * Run: node scripts/generate-icons.js
 */

const fs = require('fs');
const path = require('path');

// We'll create SVG placeholders that can be converted to PNG later
const createSVGIcon = (size) => {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="${size}" height="${size}" rx="${size * 0.1}" fill="url(#grad)"/>
  <text x="50%" y="50%" text-anchor="middle" dy=".35em" font-family="Arial, sans-serif" font-size="${size * 0.5}" fill="white" font-weight="bold">₿</text>
</svg>`;
};

const publicDir = path.join(__dirname, '../public');

// Create SVG placeholders
const sizes = [
  { size: 192, name: 'icon-192x192.svg' },
  { size: 512, name: 'icon-512x512.svg' },
  { size: 180, name: 'apple-touch-icon.svg' },
  { size: 32, name: 'favicon.svg' }
];

sizes.forEach(({ size, name }) => {
  const svg = createSVGIcon(size);
  fs.writeFileSync(path.join(publicDir, name), svg);
  console.log(`✓ Created ${name}`);
});

console.log('\n✨ SVG icons created successfully!');
console.log('\n📝 Note: For production, convert SVGs to PNGs using:');
console.log('   - Online tool: https://svgtopng.com');
console.log('   - Or install sharp: pnpm add -D sharp');
console.log('   - Or use ImageMagick: convert icon.svg icon.png');
