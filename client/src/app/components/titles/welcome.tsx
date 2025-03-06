import { UserShortInfoResponseSchema } from "@schemas/user";

export interface WelcomeTitleProps {
    user: UserShortInfoResponseSchema | null;
}

export default function WelcomeTitle(props: WelcomeTitleProps) {

    return (
        <section>
            {props.user && 
                <h1 className='text-4xl text-white-50 font-bold px-2 md:px-8'>¡Bienvenido, <span className='italic'>{props.user.name} {props.user.lastname}!</span></h1>
            }
        </section>
    );
}