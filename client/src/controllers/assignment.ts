import { CurrentSession } from "@/libs/session";
import { AssignmentService } from "@/services/assignment";
import { AssignmentSchema } from "@/schemas/assignment";

export class AssignmentController {
    static async getPendingAssignments(): Promise<AssignmentSchema[]> {
        try {
            let token = await CurrentSession.getToken();
            if (token) {
                console.log(token)
                const assignments = await AssignmentService.getPendings(token);
                return assignments;
            }
            throw new Error("Token not found");
        } catch (error) {
            console.log(error);
            return []
        }
    }
}