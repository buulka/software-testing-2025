describe('Main Page UI Rendering', () => {
    it('Проверка отображения ключевых элементов интерфейса', () => {
    cy.visit('/login');
    cy.get('input[name="login"]').type('test_user');
    cy.get('input[name="password"]').type('test_password');
    cy.contains('Войти').click();

    cy.url().should('include', '/main');
    cy.contains('Создать').should('be.visible');
    cy.contains('Фильтры').should('be.visible');
    cy.get('.table').should('exist');
    });
});
