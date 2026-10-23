interface Encounter {
    encounter_id: number;
    patient_id: number;
    risk_score: number;
    risk_level: string;
}

async function fetchEncounter(id: number): Promise<void> {
    const url =
        `https://jsonplaceholder.typicode.com/todos/${id}`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`API failed: ${response.status}`);
    }

    const data = await response.json();

    console.log("API Response:");
    console.log(JSON.stringify(data, null, 2));
}