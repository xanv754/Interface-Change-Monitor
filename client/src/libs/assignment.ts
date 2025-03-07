import { AssignmentInfoResponseSchema } from "@schemas/assignment";
import { UserShortInfoResponseSchema } from "@schemas/user";

export class AssignmentHandler {
    /**
     * Filter all assignments by a user.
     * 
     * @param {AssignmentInfoResponseSchema[]} data Assignments to filter.
     * @param {string} username Username to filter the assignments.
     * @returns {AssignmentInfoResponseSchema[]} Filtered assignments by a username.
     */
    static filterAssignmentsByUser(data: AssignmentInfoResponseSchema[], username: string){
        let dataFiltered: AssignmentInfoResponseSchema[] = [];
        data.map((assignment: AssignmentInfoResponseSchema) => {
            if (assignment.username && assignment.username === username) dataFiltered.push(assignment);
        });
        return dataFiltered;
    }

    /**
     * Get all users with have history to download.
     * 
     * @param {AssignmentInfoResponseSchema[]} data All history of assignments.
     * @returns {UserShortInfoResponseSchema[]} All users with have history to download.
     */
    static getUserWithHistory(data: AssignmentInfoResponseSchema[]): UserShortInfoResponseSchema[] {
        let dataFiltered: UserShortInfoResponseSchema[] = [];
        data.map((assignment: AssignmentInfoResponseSchema) => {
            if (assignment.username && assignment.name && assignment.lastname) {
                dataFiltered.push({
                    username: assignment.username,
                    name: assignment.name,
                    lastname: assignment.lastname,
                    profile: '',
                });
            }
        });
        return dataFiltered;
    }
}