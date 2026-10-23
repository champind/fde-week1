
interface Encounter {
    encounter_id: number;
    patient_id: number;
    risk_score: number;
    risk_level: string;
}

const encounters: Encounter[] = [
    {
        encounter_id: 101,
        patient_id: 1001,
        risk_score: 25,
        risk_level: "LOW"
    },
    {
        encounter_id: 102,
        patient_id: 1002,
        risk_score: 65,
        risk_level: "MEDIUM"
    },
    {
        encounter_id: 103,
        patient_id: 1003,
        risk_score: 90,
        risk_level: "HIGH"
    }
];

console.log(JSON.stringify(encounters, null, 2));
