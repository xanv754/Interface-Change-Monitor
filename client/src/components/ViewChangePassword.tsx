import { AdminController } from "../controllers/admin.controller";
import { UserController } from "../controllers/user.controller";
import { userType } from "../../constants/userType";
import type { AdminModel } from "../models/admin";
import type { UserModel } from "../models/user";

interface Props {
    token: string;
    user: (UserModel | AdminModel);
}

function verifyInput(firstInput: string, secondInput: string): boolean {
    let status = true;

    if (firstInput === "") {
        badInput('alertBlankPassword');
        goodInput('alertDifferentPassword');
        status = false;
    } else goodInput('alertBlankPassword');
    if (secondInput === "") {
        badInput('alertBlankRepeat');
        goodInput('alertDifferentPassword');
        status = false;
    } else goodInput('alertBlankRepeat');
    if ((firstInput !== "") && (secondInput !== "") && (firstInput !== secondInput)) {
        badInput('alertDifferentPassword');
        status = false;
    } else goodInput('alertDifferentPassword');
    return status;
}

function badInput(section: string) {
    let messageAlert = document.getElementById(section);
    messageAlert.classList.remove("hidden");
}

function goodInput(section: string) {
    let messageAlert = document.getElementById(section);
    messageAlert.classList.add("hidden");
}

function viewPassword(section: string) {
    let input = document.getElementById(section) as HTMLInputElement;
    if (section == 'password') {
        let btnView = document.getElementById('viewPassword-one');
        let btnHidden = document.getElementById('hiddenPassword-one');
        if (input.type === 'password') {
            input.type = 'text';
            btnView.classList.add('hidden');
            btnHidden.classList.remove('hidden');
        } else {
            input.type = 'password';
            btnView.classList.remove('hidden');
            btnHidden.classList.add('hidden');
        }
    } else {
        let btnView = document.getElementById('viewPassword-two');
        let btnHidden = document.getElementById('hiddenPassword-two');
        if (input.type === 'password') {
            input.type = 'text';
            btnView.classList.add('hidden');
            btnHidden.classList.remove('hidden');
        } else {
            input.type = 'password';
            btnView.classList.remove('hidden');
            btnHidden.classList.add('hidden');
        }
    }

}

export default function ViewChangePassword({ token, user }: Props){
    const updatePassword = async (newPassword: string) => {
        if (user.type == userType.admin) {
            const updated = await AdminController.updatePassword(token, user.username, newPassword);
            if (updated) {
                alert('Contraseña actualizada');
                location.href = '/admin';
            } else alert('Error al actualizar la contraseña');
        } else {
            const updated = await UserController.updatePassword(token, user.username, newPassword);
            if (updated) {
                alert('Contraseña actualizada');
                location.href = '/home';
            } else alert('Error al actualizar la contraseña');
        }
    }

    const changePasswordFormHandler = (e) => {
        e.preventDefault();
        
        const newPassword = e.target.password.value;
        const repeatPassword = e.target.repeatPassword.value;

        const status = verifyInput(newPassword, repeatPassword);
        if (status) {
            updatePassword(newPassword);
        }
    }

    return(
        <main className="w-full h-full flex justify-center items-center">
            <div className="h-fit w-40 min-w-fit px-4 py-8 bg-white rounded-xl flex flex-col items-center">
                <img src="/assets/logo.png" alt="Logo ICM" className="h-20 w-20" />
                <h2 className="font-lexend font-bold text-blue-500 text-3xl mb-4 text-center">Cambio de Contraseña</h2>
                <form onSubmit={changePasswordFormHandler} className="w-full flex flex-col gap-2 px-4">
                    <div className="flex flex-col w-full max-md:flex-col">
                        <div className="flex flex-row w-full max-md:flex-col">
                            <label htmlFor="password" className="w-70 py-2 px-4 bg-blue-500 md:rounded-l-md text-white text-center font-lexend max-md:rounded-t-md max-md:w-full">Nueva Contraseña</label>
                            <div className="flex flex-row w-full">
                                <input id="password" name="password" type="password" className="w-full outline-none text-blue-500 font-lexend p-2 bg-gray-550 max-md:rounded-bl-md max-md:w-full" placeholder="Contraseña" />
                                <button type="button" id="viewPassword-one" className="p-1 bg-gray-550 md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('password')}}>    
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                                        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                    </svg>
                                </button>
                                <button type="button" id="hiddenPassword-one" className="p-1 hidden bg-gray-550 md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('password')}}>    
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye-slash" viewBox="0 0 16 16">
                                        <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z"/>
                                        <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
                                        <path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12z"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <small id="alertBlankPassword" className="px-2 font-lexend font-light text-red-100 hidden my-1">Contraseña requerida</small>
                    </div>
                    <div className="flex flex-col w-full max-md:flex-col">
                        <div className="flex flex-row w-full max-md:flex-col">
                            <label htmlFor="repeatPassword" className="w-70 py-2 px-4 bg-blue-500 md:rounded-l-md text-white text-center font-lexend max-md:rounded-t-md max-md:w-full">Confirmar Contraseña</label>
                            <div className="flex flex-row w-full">
                                <input id="repeat" name="repeatPassword" type="password" className="w-full outline-none text-blue-500 font-lexend p-2 bg-gray-550 max-md:rounded-bl-md max-md:w-full" placeholder="Contraseña" />
                                <button type="button" id="viewPassword-two" className="p-1 bg-gray-550 md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('repeat')}}>    
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                                        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                    </svg>
                                </button>
                                <button type="button" id="hiddenPassword-two" className="p-1 hidden bg-gray-550 md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('repeat')}}>    
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye-slash" viewBox="0 0 16 16">
                                        <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z"/>
                                        <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
                                        <path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12z"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <small id="alertBlankRepeat" className="px-2 font-lexend font-light text-red-100 hidden my-1">Contraseña requerida</small>
                        <small id="alertDifferentPassword" className="text-center font-lexend font-light text-red-100 hidden my-1">Las contraseñas deben coincidir</small>
                    </div>
                    <div className="w-full flex flex-row justify-center items-center gap-2 mt-2 max-md:flex-col">
                        {user.type == userType.user && <button id="btn-cancel" type="button" className="rounded-full font-lexend font-bold text-white bg-blue-500 px-6 py-2 transition-all duration-300 ease-in-out hover:bg-red-500 max-md:w-full" onClick={() => {location.href = '/user/history'}}>Cancelar</button>}
                        {user.type == userType.admin && <button id="btn-cancel" type="button" className="rounded-full font-lexend font-bold text-white bg-blue-500 px-6 py-2 transition-all duration-300 ease-in-out hover:bg-red-500 max-md:w-full" onClick={() => {location.href = '/admin/profile'}}>Cancelar</button>}
                        <button id="btn-save" type="submit" className="rounded-full font-lexend font-bold text-white bg-blue-500 px-6 py-2 transition-all duration-300 ease-in-out hover:bg-green-500 max-md:w-full">Cambiar</button>
                    </div>
                </form>
            </div>
        </main>
    );
}