describe('Prueba del Sistema Predictivo', () => {
  it('Debe analizar el riesgo de un estudiante correctamente', () => {
    // 1. Entra a tu página de Vercel
    cy.visit('https://sistema-predictivo-academico.vercel.app/'); 
    
    // 2. Borra TODO y escribe el ID que sabes que existe
    cy.get('input[type="number"]').type('{selectall}{backspace}1');
    
    // 3. Hace clic en el botón azul
    cy.contains('Analizar Desempeño').click();
    
    // 4. Verifica que aparezca el resultado (con paciencia)
    cy.contains('Resultados para:', { timeout: 60000 }).should('be.visible');
  })
})