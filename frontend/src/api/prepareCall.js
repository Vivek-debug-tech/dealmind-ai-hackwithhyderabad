/**
 * prepareCall(dealId, mode)
 */
export async function prepareCall(dealId, mode = "both") {
  const response = await fetch('/api/prepare/comparison', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      deal_id: dealId,
      query: "Prepare me for my next call with Acme.",
      mode: mode
    }),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Failed to prepare call: ${response.status} ${errText}`);
  }
  return response.json();
}
