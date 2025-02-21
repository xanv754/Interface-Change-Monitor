'use client';

import { SystemController } from "@/controllers/system";
import { AssignmentController } from "@/controllers/assignment";
import { CurrentSession } from "@/libs/session";
import { UserInfoSchema } from "@/schemas/user";
import { ProfileTypes } from "@/libs/types";
import { useEffect, useState } from "react";

export default function Test() {

    const getData = async () => {
        const user = await CurrentSession.getInfo();
        const configuration = await SystemController.getConfiguration();
        if (configuration) {
            console.log(configuration);
            if (user?.profile === ProfileTypes.admin) {
                if (configuration.canReceiveAssignment.ADMIN) {
                    const data = await AssignmentController.getPendingAssignments();
                    console.log(data);
                }
            }
        }
    }

    useEffect(() => {
        getData();
    }, [])

    return (
        <div>
            <h1>Test!</h1>
        </div>
    );
}