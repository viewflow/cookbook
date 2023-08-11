export class MyTotalCountComponent extends HTMLElement {
  private form: HTMLFormElement | null = null;

  connectedCallback() {
    this.form = this.closest('form');

    if (this.form) {
      this.form.addEventListener('input', this.handleInputChange);
    }

    this.calculate();
  }

  disconnectedCallback() {
    if (this.form) {
      this.form.removeEventListener('input', this.handleInputChange);
    }
  }

  handleInputChange = () => {
    this.calculate();
  }

  calculate() {
    let rawExpression = this.getAttribute('expression');
    let targetName = this.getAttribute('target');

    if (!targetName) {
        console.warn('No target attribute provided.');
        return;
    }

    const targetInput = this.closest('form')?.querySelector(`input[name="${targetName}"]`) as HTMLInputElement;

    if (!targetInput) {
        console.warn(`No input found with the name: ${targetName}`);
        return;
    }

    if (this.isValidExpression(rawExpression)) {
        let result = this.evaluateExpression(rawExpression!);
        targetInput.value = result.toString();
    } else {
        targetInput.value = 'Error: Invalid expression';
    }
  }

  isValidExpression(expr: string | null): boolean {
    if (!expr) return false;
    const pattern = /^[a-zA-Z0-9_]+([+*][a-zA-Z0-9_]+)*$/;
    return pattern.test(expr);
  }

  evaluateExpression(expr: string): number {
    let parts = expr.split('+').map(part => {
      if (part.includes('*')) {
        return part.split('*').reduce((acc, operand) => {
          const inputElement = this.form!.querySelector(`input[name="${operand}"]`) as HTMLInputElement;
          const operandValue = parseFloat(inputElement?.value || "0");
          return acc * operandValue;
        }, 1);
      } else {
        const inputElement = this.form!.querySelector(`input[name="${part}"]`) as HTMLInputElement;
        return parseFloat(inputElement?.value || "0");
      }
    });

    // Then handle addition
    return parts.reduce((sum, val) => sum + val, 0);
  }
}
