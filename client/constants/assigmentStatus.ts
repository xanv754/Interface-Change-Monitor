class AssigmentStatus {
    default: string = "Sin Asignación";
    pending: string = "Asignado sin revisión";
    reviewed: string = "Revisado - Interfaz sin necesidad de redescubrimiento";
    rediscovered: string = "Revisado - Interfaz redescubierta";
}

export const assignmentStatus = new AssigmentStatus();