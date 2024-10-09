export class ErrorRequest extends Error {
    status: String

    constructor(status: String) {
        if (status == '400') {
            super('Bad Requests');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else if (status == '401') {
            super('Unauthorized user');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else if (status == '404') {
            super('Not Found');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else if (status == '409') {
            super('User conflict');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else if (status == '500') {
            super('Internal Server Error');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else if (status == '503') {
            super('Service Unavailable');
            this.status = status;
            this.name = 'ErrorRequests';
        }
        else {
            super('Error Requests');
            this.status = status;
            this.name = 'ErrorRequests';
        }
    }
}