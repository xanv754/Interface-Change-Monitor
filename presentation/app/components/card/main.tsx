import Image from "next/image";

export enum StatusOption {
    NORMAL = 'NORMAL',
    PENDING = 'PENDING',
    REVIEW = 'REVIEW',
}

const ACCENT_BORDER: Record<StatusOption, string> = {
    [StatusOption.NORMAL]: 'border-l-(--blue)',
    [StatusOption.PENDING]: 'border-l-(--yellow)',
    [StatusOption.REVIEW]: 'border-l-(--green)',
};

const ACCENT_CHIP: Record<StatusOption, string> = {
    [StatusOption.NORMAL]: 'bg-(--blue-tint)',
    [StatusOption.PENDING]: 'bg-(--yellow-light)',
    [StatusOption.REVIEW]: 'bg-(--green-light)',
};

/**
 * Component to show a card with a title, total and status.
 *
 * @param title - Title of the card.
 * @param total - Total number of interfaces.
 * @param status - Status of the card.
 */
interface CardProps {
    title: string;
    total: number;
    status: StatusOption;
}

export default function CardComponent(content: CardProps) {
    return (
        <div className={`card ${ACCENT_BORDER[content.status]} border-l-4 m-0 w-[25vw] min-w-fit p-4 flex flex-col flex-nowrap gap-3`}>
            <section className="flex gap-3 flex-row items-center">
                <span className={`${ACCENT_CHIP[content.status]} flex items-center justify-center rounded-[var(--radius)] p-2`}>
                    {content.status === StatusOption.NORMAL && <Image
                        src="/statistics/normal.svg"
                        alt="Statistics"
                        width={20}
                        height={20}
                    />}
                    {content.status === StatusOption.PENDING && <Image
                        src="/statistics/pending.svg"
                        alt="Statistics Pending"
                        width={20}
                        height={20}
                    />}
                    {content.status === StatusOption.REVIEW && <Image
                        src="/statistics/review.svg"
                        alt="Statistics Review"
                        width={20}
                        height={20}
                    />}
                </span>
                <h2 className="m-0 text-sm font-medium text-(--gray)">{content.title}</h2>
            </section>
            <section>
                <p className="font-display m-0 text-3xl font-semibold text-(--ink)">{content.total}</p>
            </section>
        </div>
    );
}
