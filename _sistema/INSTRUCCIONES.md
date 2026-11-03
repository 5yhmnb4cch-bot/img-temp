# Instagram Goodfellas — proceso diario (versión nube, sin la compu de Facu)

Cuenta: @gf.tuning · Metricool brand/blogId 7810034 · zona horaria America/Buenos_Aires.
Repo de trabajo: GitHub 5yhmnb4cch-bot/img-temp (público: acá NO van precios, costos, proveedores ni datos privados).
- `_sistema/` → estas instrucciones, marcas.md (reglas de marcas/autos/variedad), publicados.csv, carrusel.py + lobo.svg (plantilla), ejemplo_spec.json, indice_gf.csv (códigos GF: codigo, marca_auto, modelo, articulo, seccion, nombre_original).
- `posts/<fecha>/` → slides temporales. Se borran apenas Metricool las toma.

## Cada noche (armar los posteos de MAÑANA, 10:00 y 18:00)
0. Preparar: add_repo (owner 5yhmnb4cch-bot, repo img-temp, access push) → `git clone --depth 1 https://github.com/5yhmnb4cch-bot/img-temp /home/claude/img-temp` (timeout largo). git config user.name "Goodfellas", user.email "facuamoedo@gmail.com". `pip install openpyxl` si hace falta; Playwright y Chromium ya están.
1. Leer `_sistema/marcas.md` y `_sistema/publicados.csv`. Revisar en Metricool (getScheduledPosts) que mañana no haya posteos ya programados; si hay, no duplicar.
2. Elegir 2 productos (reglas de variedad de marcas.md: no repetir marca de auto ni de pieza el mismo día; no repetir categoría ni marca de pieza en días seguidos; solo autos que se venden en Argentina; nada de RS6/RS7; pedidos especiales vigentes).
   Buscar el código GF en `_sistema/indice_gf.csv` (por modelo + nombre_original). Si no tiene código, avisarle a Facu en el mensaje para que lo cargue (y poner "Ref. GF-____").
3. Fotos: desde la página del proveedor. Sitios accesibles desde la nube:
   - ind-distribution.com (Shopify: `<url-producto>.json`; reescribir `https://cdn.shopify.com/s/files/1/<n>/<n>/<n>/(products|files)/X` → `https://ind-distribution.com/cdn/shop/(products|files)/X`).
   - baanvelgen.com (Shopify; distribuidor oficial de iPE y vende Novitec): buscar con `https://baanvelgen.com/search/suggest.json?q=<texto>&resources%5Btype%5D=product&resources%5Blimit%5D=10`, ficha en `/products/<handle>.json`, imágenes reescritas a `https://baanvelgen.com/cdn/shop/(products|files)/X`. Usarlo para posteos de iPE (escapes) y Novitec (Ferrari, Lamborghini, McLaren).
   - 034motorsport.com (páginas de producto, imágenes en "full":"…jpg") y pp-performance.de.
   - ECS Tuning NO se puede desde la nube (su web bloquea accesos automáticos). Para productos ECS, elegir el mismo tipo de pieza de otro proveedor o dejarlo para las tandas armadas con la compu de Facu.
   - Sin marcas de agua IND/ECS (pintar de blanco el rincón en fotos de fondo blanco; si la foto tiene fondo, recortar o descartar). Patentes legibles: difuminar.
   - Portada: el AUTO con la pieza. Revisar CADA slide (pieza entera, bien encuadrada, nada cortado).
4. Carrusel con `python3 _sistema/carrusel.py spec.json out/` (copiar lobo.svg junto a carrusel.py). 5 slides:
   portada · doble (instalado) · doble (detalle/producto) · beneficios ("¿Qué ganás?", 3 ítems; `dato` = cifra SOLO si está verificada en la web de la marca, si no 01/02/03) · cierre (lo genera la plantilla: "Cotizá tus piezas y repuestos con nosotros" + WhatsApp 11 5135-9817 + DM).
   - Portada: título = tipo de pieza; bajada pro = material/tecnología · marca/línea. Textos de fotos: `kicker` corto + frase elegante (nada simplón tipo "Así queda instalado").
   - Logo Goodfellas en todas las slides (la plantilla ya lo hace).
5. Descripción (formato fijo):
   <Pieza> <marca/línea> para <auto> 🔥
   (vacía) 2-3 líneas profesionales en rioplatense
   (vacía) 3 líneas "✔️ ..."
   (vacía) "📲 Cotizá tus piezas y repuestos con nosotros" / "💬 WhatsApp 11 5135-9817 o por DM"
   (vacía) hashtags
   (vacía) "." / "." / "." y al final "Ref. GF-XXXX" (SOLO el código Goodfellas, nunca el número de pieza de la marca). Nunca precio. Verificar datos técnicos en la web de la marca/proveedor.
6. Subir slides: copiar a `posts/<fecha>/<hora>_<producto>_NN.jpg`, commit y `git push origin HEAD:main` (antes `git fetch origin main` + rebase).
   URLs: `https://raw.githubusercontent.com/5yhmnb4cch-bot/img-temp/main/posts/<fecha>/<archivo>`.
   Programar en Metricool (createScheduledPost, autoPublish=true, tipo POST, solo Instagram). Confirmar que la respuesta trae media en static.metricool.com.
   Después: `git rm -r posts/<fecha>` + commit + push (las imágenes no quedan en el repo).
7. Avisar a Facu: PushNotification corta + SendUserMessage con la vista previa de los 2 carruseles (tira de miniaturas con SendUserFile), horario y texto de cada descripción. Recordar: si no responde se publican solos; si quiere un cambio, que lo diga en esa conversación.
8. Agregar los 2 productos a `_sistema/publicados.csv` (fecha, hora, código GF, marca, producto, auto, id Metricool), commit y push.
Si algo falla y no se pueden programar, avisar por push qué pasó. Si Facu pide un cambio, rehacer slides/texto y actualizar (updateScheduledPost) el post en Metricool.
