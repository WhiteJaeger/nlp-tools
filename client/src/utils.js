export async function fetchAndSetData(url, setFunction) {
    const response = await fetch(
        url,
    );
    setFunction(await response.json());
}

export async function postAndGetResponse(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}
