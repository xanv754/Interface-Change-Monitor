export interface NewAssignmentSchema {
  old_interface_id: number;
  current_interface_id: number;
  username: string;
  assign_by: string;
  type_status: string;
}

export interface ReassignmentSchema {
  old_interface_id: number;
  current_interface_id: number;
  old_username: string;
  new_username: string;
  assign_by: string;
}

export interface UpdateAssignmentSchema {
  old_interface_id: number;
  current_interface_id: number;
  type_status: string;
}

export interface StatisticsAssignmentSchema {
  total_pending_today: number;
  total_inspected_today: number;
  total_rediscovered_today: number;
  total_pending_month: number;
  total_inspected_month: number;
  total_rediscovered_month: number;
  username: string;
  name: string;
  lastname: string;
}