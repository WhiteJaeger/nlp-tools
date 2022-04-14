export async function fetchAndSetData(url, setFunction) {
    const response = await fetch(
        url,
    );
    setFunction(await response.json());
}