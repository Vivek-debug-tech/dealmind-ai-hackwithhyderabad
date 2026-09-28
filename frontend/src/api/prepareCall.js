/**
 * prepareCall(dealId)
 */
export async function prepareCall(dealId) {
  const response = await fetch('/api/prepare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ deal_id: dealId }),
  });

  if (!response.ok) throw new Error('Failed to prepare call');
  return response.json();
}
