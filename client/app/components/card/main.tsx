import Image from "next/image";
import styles from './card.module.css';

export enum StatusOption {
    NORMAL = 'NORMAL',
    PENDING = 'PENDING',
    REVIEW = 'REVIEW',
}

interface CardProps {
    title: string;
    total: number;
    status: StatusOption;
}

export default function CardComponent(content: CardProps) {
    return (
        <div className={`${content.status === StatusOption.NORMAL ? 'bg-(--blue)' : ''} ${content.status === StatusOption.PENDING ? 'bg-(--yellow)' : ''} ${content.status === StatusOption.REVIEW ? 'bg-(--green)' : ''} m-0 w-[25vw] min-w-fit text-(--white) p-4 rounded-lg flex flex-col flex-nowrap shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]`}>
            <section className="flex gap-3.5 flex-row">
                {content.status === StatusOption.NORMAL && <Image
                    src="/statistics/normal.svg"
                    alt="Statistics"
                    width={24}
                    height={24}
                />}
                {content.status === StatusOption.PENDING && <Image
                    src="/statistics/pending.svg"
                    alt="Statistics Pending"
                    width={24}
                    height={24}
                />}
                {content.status === StatusOption.REVIEW && <Image
                    src="/statistics/review.svg"
                    alt="Statistics Review"
                    width={24}
                    height={24}
                />}
                <h2 className="m-0 text-lg">{content.title}</h2>
            </section>
            <section>
                <p className="m-0 text-3xl font-bold">{content.total}</p>
            </section>
        </div>
    );
}