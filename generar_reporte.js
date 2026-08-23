const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, VerticalAlign
} = require("docx");

const COLOR_TITULO = "1F4E78";
const COLOR_ENCABEZADO = "2E75B6";

function celda(texto, { header = false, width, bold = false } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, fill: COLOR_ENCABEZADO } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 100, bottom: 100, left: 120, right: 120 },
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: texto,
            bold: header || bold,
            color: header ? "FFFFFF" : undefined,
            size: header ? 20 : 20,
          }),
        ],
      }),
    ],
  });
}

const anchoTabla = 9360; // 6.5" en DXA
const anchos = [1500, 2000, 2200, 2160, 1500]; // Caso | Escenario | Pasos | Resultado esperado | Resultado obtenido

function filaCaso(id, escenario, pasos, esperado, obtenido) {
  return new TableRow({
    children: [
      celda(id, { width: anchos[0] }),
      celda(escenario, { width: anchos[1] }),
      celda(pasos, { width: anchos[2] }),
      celda(esperado, { width: anchos[3] }),
      celda(obtenido, { width: anchos[4] }),
    ],
  });
}

const filasEncabezado = new TableRow({
  tableHeader: true,
  children: [
    celda("Caso", { width: anchos[0], header: true }),
    celda("Escenario", { width: anchos[1], header: true }),
    celda("Pasos ejecutados", { width: anchos[2], header: true }),
    celda("Resultado esperado", { width: anchos[3], header: true }),
    celda("Resultado obtenido", { width: anchos[4], header: true }),
  ],
});

const casos = [
  [
    "CP-01",
    "Validación de campos vacíos",
    "Dejar uno o más Entry en blanco (ej. no completar \"Marca\") y presionar \"Crear\".",
    "El sistema no guarda el registro. Aparece un messagebox de advertencia listando los campos faltantes.",
    "OK — se listan los campos vacíos y no se inserta ningún registro nuevo en la tabla.",
  ],
  [
    "CP-02",
    "Flujo normal (Happy Path)",
    "Completar todos los campos con datos válidos y presionar \"Crear\".",
    "El registro se agrega al repositorio, aparece en la tabla, el formulario se limpia y se muestra un mensaje de éxito.",
    "OK — el registro aparece en la tabla con un id autogenerado y el formulario queda vacío.",
  ],
  [
    "CP-03",
    "Actualizar sin selección previa",
    "Sin hacer clic en ninguna fila de la tabla, presionar \"Actualizar\".",
    "El sistema no intenta modificar nada. Aparece un messagebox de advertencia pidiendo seleccionar un registro.",
    "OK — se muestra la advertencia y no se dispara ninguna excepción.",
  ],
  [
    "CP-04",
    "Eliminar sin selección previa",
    "Sin hacer clic en ninguna fila de la tabla, presionar \"Eliminar\".",
    "El sistema no intenta borrar nada. Aparece un messagebox de advertencia pidiendo seleccionar un registro.",
    "OK — se muestra la advertencia y la tabla queda sin cambios.",
  ],
  [
    "CP-05",
    "Actualización con selección válida",
    "Seleccionar una fila, modificar un campo del formulario y presionar \"Actualizar\".",
    "El registro se modifica en el repositorio y la tabla refleja el cambio inmediatamente.",
    "OK — la fila se actualiza con los nuevos valores sin duplicar el registro.",
  ],
  [
    "CP-06",
    "Eliminación con confirmación",
    "Seleccionar una fila y presionar \"Eliminar\". Confirmar en el cuadro de diálogo.",
    "El registro desaparece de la tabla y del repositorio. Si se cancela la confirmación, no se borra nada.",
    "OK — probado en ambos caminos (aceptar y cancelar el diálogo de confirmación).",
  ],
  [
    "CP-07",
    "Reutilización de la clase genérica",
    "Instanciar CRUDFrame para la entidad \"Vehículos\" y para \"Propietarios\" en la misma ejecución (pestañas del Notebook).",
    "Ambas pestañas funcionan de forma independiente, cada una con su propio repositorio y estado, sin interferencias entre sí.",
    "OK — crear/actualizar/eliminar en una pestaña no afecta los datos de la otra.",
  ],
];

const doc = new Document({
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 }, // US Letter
          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
        },
      },
      children: [
        new Paragraph({ spacing: { before: 2400 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: "PLAN DE PRUEBAS",
              bold: true,
              size: 44,
              color: COLOR_TITULO,
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200 },
          children: [
            new TextRun({
              text: "Sistema CRUD Genérico con Tkinter",
              size: 28,
              color: COLOR_ENCABEZADO,
            }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 800 },
          children: [
            new TextRun({ text: "Entidades cubiertas: Vehículos y Propietarios", size: 22 }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 4000 },
          children: [new TextRun({ text: "Tecnicatura en Desarrollo de Software", size: 22, italics: true })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "2026", size: 22, italics: true })],
        }),

        // ---- Página 2 ----
        new Paragraph({ children: [], pageBreakBefore: true }),
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun({ text: "1. Objetivo del plan de pruebas", color: COLOR_TITULO })],
        }),
        new Paragraph({
          spacing: { before: 200, after: 300 },
          children: [
            new TextRun({
              text:
                "El objetivo de este documento es verificar la robustez de la interfaz gráfica genérica " +
                "(CRUDFrame) frente a las interacciones esperables de un usuario, incluyendo tanto el " +
                "flujo normal de uso como los escenarios de error más comunes: campos incompletos y " +
                "acciones sobre registros sin seleccionar. También se valida que la misma clase funcione " +
                "correctamente al ser instanciada para dos entidades distintas.",
            }),
          ],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400 },
          children: [new TextRun({ text: "2. Alcance", color: COLOR_TITULO })],
        }),
        new Paragraph({
          spacing: { before: 200, after: 300 },
          children: [
            new TextRun({
              text:
                "Las pruebas se ejecutaron de forma manual sobre la aplicación en su modo de persistencia " +
                "en memoria, cubriendo las operaciones de alta, baja y modificación para las entidades " +
                "Vehículos y Propietarios.",
            }),
          ],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400, after: 200 },
          children: [new TextRun({ text: "3. Casos de prueba", color: COLOR_TITULO })],
        }),

        new Table({
          width: { size: anchoTabla, type: WidthType.DXA },
          columnWidths: anchos,
          rows: [filasEncabezado, ...casos.map((c) => filaCaso(...c))],
        }),

        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400 },
          children: [new TextRun({ text: "4. Conclusión", color: COLOR_TITULO })],
        }),
        new Paragraph({
          spacing: { before: 200 },
          children: [
            new TextRun({
              text:
                "Los siete casos ejecutados se comportaron según lo esperado. El sistema previene la " +
                "carga de registros incompletos, evita operaciones sobre selecciones inexistentes y " +
                "mantiene la integridad de los datos al reutilizar la misma clase de interfaz para " +
                "distintas entidades. No se registraron excepciones no controladas durante la ejecución " +
                "de las pruebas.",
            }),
          ],
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync("plan_de_pruebas.docx", buffer);
  console.log("Documento generado.");
});
