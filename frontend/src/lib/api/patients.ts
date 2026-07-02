import { api } from "./client";

export interface Patient {
  id: string;
  nida_id?: string;
  given_name?: string;
  family_name?: string;
  sex?: string;
  birth_date?: string;
}

export interface PatientSearchResponse {
  results: Patient[];
  next_cursor?: string | null;
}

export const searchPatients = (q: string) =>
  api<PatientSearchResponse>(`/patients?q=${encodeURIComponent(q)}`);

export interface PatientRegister {
  nida_id: string;
  given_name?: string;
  family_name?: string;
  sex?: string;
  birth_date?: string;
}

export const registerPatient = (data: PatientRegister) =>
  api<Patient>("/patients", { method: "POST", body: JSON.stringify(data) });
