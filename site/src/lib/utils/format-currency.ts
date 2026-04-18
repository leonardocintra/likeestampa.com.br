/**
 * Formats a value in cents to BRL currency
 * @param valueInCents - Value in cents (e.g., 2999 for R$ 29,99)
 * @returns Formatted BRL string (e.g., "R$ 29,99")
 */
export function formatCurrency(valueInCents: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valueInCents / 100);
}

/**
 * Formats a percentage value
 * @param value - Percentage value (e.g., 0.15 for 15%)
 * @returns Formatted percentage string (e.g., "15%")
 */
export function formatPercentage(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "percent",
  }).format(value);
}

/**
 * Formats a number with thousand separators
 * @param value - Number to format
 * @returns Formatted number string
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("pt-BR").format(value);
}
