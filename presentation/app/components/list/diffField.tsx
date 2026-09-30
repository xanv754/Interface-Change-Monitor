/**
 * Presentational helper that renders a single field of an interface change:
 * the value once if it did not change, or as `old → new` if it did.
 *
 * @param label - Label of the field.
 * @param oldValue - Previous value of the field.
 * @param newValue - Current value of the field.
 */
interface DiffFieldProps {
  label: string;
  oldValue: string;
  newValue: string;
}

export default function DiffField({ label, oldValue, newValue }: DiffFieldProps) {
  const changed = oldValue !== newValue;
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs font-medium text-(--gray)">{label}</span>
      {changed ? (
        <span className="font-mono text-sm">
          <span className="text-(--gray) line-through decoration-(--gray-light)">{oldValue}</span>
          <span className="mx-1.5 text-(--gray)">→</span>
          <span className="text-(--red) font-medium">{newValue}</span>
        </span>
      ) : (
        <span className="font-mono text-sm text-(--ink)">{newValue}</span>
      )}
    </div>
  );
}
