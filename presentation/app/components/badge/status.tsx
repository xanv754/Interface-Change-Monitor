import { AssignmentStatusTypes } from "@/constants/types";

const STATUS_LABELS: Record<string, string> = {
  [AssignmentStatusTypes.PENDING]: "Pendiente",
  [AssignmentStatusTypes.INSPECTED]: "Revisado",
  [AssignmentStatusTypes.REDISCOVERED]: "Revisado (Interfaz Redescubierta)",
  [AssignmentStatusTypes.EQUIPMENT_DOWN]: "Equipo Caído",
};

const STATUS_CLASSES: Record<string, string> = {
  [AssignmentStatusTypes.PENDING]: "badge-pending",
  [AssignmentStatusTypes.INSPECTED]: "badge-ok",
  [AssignmentStatusTypes.REDISCOVERED]: "badge-info",
  [AssignmentStatusTypes.EQUIPMENT_DOWN]: "badge-danger",
};

/**
 * Component to show the status of an assignment as a colored badge.
 *
 * @param status - Assignment status to display.
 */
interface StatusBadgeProps {
  status: string;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span className={`badge ${STATUS_CLASSES[status] ?? "badge-pending"}`}>
      {STATUS_LABELS[status] ?? status}
    </span>
  );
}
