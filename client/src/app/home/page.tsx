'use client';

import { Routes } from "@/libs/routes";
import { CurrentSession } from "@/libs/session";
import { ProfileTypes } from "@/libs/types";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

export default function HomeView() {
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        const user = CurrentSession.getInfoUser();
        if (user) {
            if (user.profile === ProfileTypes.root || user.profile === ProfileTypes.soport) {
                router.push(Routes.homeAssign);
            } else if (user.profile === ProfileTypes.standard || user.profile === ProfileTypes.admin) {
                router.push(Routes.homeAssigned);
            }
        }
        else router.push(Routes.login);
    }, [pathname]);

    return (
        <></>
    );
}