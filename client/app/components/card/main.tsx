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
        <div className={`${styles.card} ${content.status === StatusOption.NORMAL ? styles.cardNormal : ''} ${content.status === StatusOption.PENDING ? styles.cardPending : ''} ${content.status === StatusOption.REVIEW ? styles.cardReview : ''}`}>
            <section className={styles.cardTitle}>
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
                <h2>{content.title}</h2>
            </section>
            <section className={styles.cardContent}>
                <p>{content.total}</p>
            </section>
        </div>
    );
}