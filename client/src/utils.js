import {API_BASE_URL} from "./constants";


export async function fetchAndSetData(url, setFunction) {
    const response = await fetch(
        `${API_BASE_URL}/${url}`,
    );
    setFunction(await response.json());
}

export async function postAndGetResponse(url, data) {
    const response = await fetch(`${API_BASE_URL}/${url}`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

export async function fetchImage(imageName) {
    const response = await fetch(`${API_BASE_URL}/images/${imageName}`);
    const blob = await response.blob();
    return URL.createObjectURL(blob);
}
