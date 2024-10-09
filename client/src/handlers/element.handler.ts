import type { Element } from '../models/element';
import { ErrorRequest } from '../class/Error';

class HandlerRequestElement {
  private url: string = import.meta.env.PUBLIC_API;

  async getElementsToday(token: string): Promise<Element[] | ErrorRequest>  {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/elements`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      const interfaces: Element[] = await response.json();
      return interfaces;
    } catch (error) {
      return error;
    }
  }

  async getElements(token: string): Promise<Element[] | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/elements/backup`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      const interfaces: Element[] = await response.json();
      return interfaces;
    } catch (error) {
      return error;
    }
  }

  async getElement(token: string, id: string): Promise<Element | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/elements/id=${id}`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      const current_interface: Element = await response.json();
      return current_interface;
    } catch (error) {
      return error;
    }
  }

}

export const ElementRequest = new HandlerRequestElement();
