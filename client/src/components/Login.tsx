import { LoginController } from "../controllers/login.controller";
import type { RegisterModel } from "../models/register";
import { userType } from "../../constants/userType";
import type { LoginModel } from "../models/login";
import { Zoom } from "react-awesome-reveal";
import { useCookies } from 'react-cookie'

function validatorLogin(user: string, password: string): boolean {
    const regex = /[^a-zA-Z0-9\s]/;
    let status: boolean = true;
    if (user) {
        const alertUser = document.getElementById("alertUser");
        alertUser.classList.add("hidden");
        if (regex.test(user)) {
            const alertUserRegex = document.getElementById("alertUserRegex");
            alertUserRegex.classList.remove("hidden");
            status = false;
        } else {
            const alertUserRegex = document.getElementById("alertUserRegex");
            alertUserRegex.classList.add("hidden");
        }

    } else if (!user) {
        const alertUser = document.getElementById("alertUser");
        const alertUserRegex = document.getElementById("alertUserRegex");
        alertUserRegex.classList.add("hidden");
        alertUser.classList.remove("hidden");
        status = false;
    }
    if (password) {
        const alertPassword = document.getElementById("alertPassword");
        alertPassword.classList.add("hidden");
    } else if (!password) {
        const alertPassword = document.getElementById("alertPassword");
        alertPassword.classList.remove("hidden");
        status = false;
    }

    return status;
}

function validatorRegister(user: string, password: string, name:string, lastname:string, userType: string): boolean {
    const regex = /[^a-zA-Z0-9\s]/;
    let status: boolean = true;
    const alertRepeatUser = document.getElementById("alertRepeatUser");
    if (!alertRepeatUser.classList.contains("hidden")) alertRepeatUser.classList.add("hidden");
    if (user) {
        const alertUser = document.getElementById("alertUser");
        alertUser.classList.add("hidden");
        if (regex.test(user)) {
            const alertUserRegex = document.getElementById("alertUserRegex");
            alertUserRegex.classList.remove("hidden");
            status = false;
        } else {
            const alertUserRegex = document.getElementById("alertUserRegex");
            alertUserRegex.classList.add("hidden");
        }

    } else if (!user) {
        const alertUser = document.getElementById("alertUser");
        const alertUserRegex = document.getElementById("alertUserRegex");
        alertUserRegex.classList.add("hidden");
        alertUser.classList.remove("hidden");
        status = false;
    }
    if (password) {
        const alertPassword = document.getElementById("alertPassword");
        alertPassword.classList.add("hidden");
    } else if (!password) {
        const alertPassword = document.getElementById("alertPassword");
        alertPassword.classList.remove("hidden");
        status = false;
    }
    if (name) {
        const alertName = document.getElementById("alertName");
        alertName.classList.add("hidden");
        if (regex.test(name)) {
            const alertNameRegex = document.getElementById("alertNameRegex");
            alertNameRegex.classList.remove("hidden");
            status = false;
        } else {
            const alertNameRegex = document.getElementById("alertNameRegex");
            alertNameRegex.classList.add("hidden");
        }
    } else if (!name) {
        const alertName = document.getElementById("alertName");
        const alertNameRegex = document.getElementById("alertNameRegex");
        alertNameRegex.classList.add("hidden");
        alertName.classList.remove("hidden");
        status = false;
    }
    if (lastname) {
        const alertLastname = document.getElementById("alertLastname");
        alertLastname.classList.add("hidden");
        if (regex.test(lastname)) {
            const alertLastnameRegex = document.getElementById("alertLastnameRegex");
            alertLastnameRegex.classList.remove("hidden");
            status = false;
        } else {
            const alertLastnameRegex = document.getElementById("alertLastnameRegex");
            alertLastnameRegex.classList.add("hidden");
        }
    } else if (!lastname) {
        const alertLastname = document.getElementById("alertLastname");
        const alertLastnameRegex = document.getElementById("alertLastnameRegex");
        alertLastnameRegex.classList.add("hidden");
        alertLastname.classList.remove("hidden");
        status = false;
    }
    if (userType) {
        const alertUserType = document.getElementById("alertUserType");
        alertUserType.classList.add("hidden");
    } else if (!userType) {
        const alertUserType = document.getElementById("alertUserType");
        alertUserType.classList.remove("hidden");
        status = false;
    }

    return status;
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

function existingUser(): void {
    const alert = document.getElementById("alertRepeatUser");
    alert.classList.toggle("hidden");
}

function invalidUser(): void {
    const alert = document.getElementById("alertInvalidUser");
    alert.classList.remove("hidden");
}

function validUser(): void {
    const alert = document.getElementById("alertInvalidUser");
    alert.classList.add("hidden");
}

async function sendRegister(userData: RegisterModel) {
    const status = await LoginController.register(userData);
    if (status == 1) {
        alert("Registro éxitoso. La petición de registro ha sido enviada al administrador. Espere su confirmación para poder iniciar sesión");
        location.href = "/";
    } else if (status == 2) {
        existingUser();
    } else {
        alert("Error al registrar");
    }
}

export default function Form({ modo }){  

    const [cookies, setCookies] = useCookies(['token', 'type']);
    
    const sendLogin = async (userData: LoginModel) => {
        const response = await LoginController.login(userData);
        if (!response) {
            invalidUser();
            return null;
        } else {
            validUser();
            let token = response.access_token;
            const user = await LoginController.getDataUser(token);
            if (!user) invalidUser();
            else {
                setCookies('token', token);
                setCookies('type', user.type);
                if (user.type == userType.admin) location.href = "/admin"
                else if (user.type == userType.user) location.href = "/home"
            }
        }
    }
    
    const formHandler = (e) => {
        e.preventDefault();

        if (modo == "login") {
            const username = e.target.user.value;
            const password = e.target.password.value;
    
            let statusValidator = validatorLogin(username, password);
    
            if (statusValidator) {
                const userData: LoginModel = {
                    "user": username,
                    "password": password
                }
                sendLogin(userData);
            }
        } else {
            const username = e.target.user.value;
            const password = e.target.password.value;
            const name = e.target.name.value;
            const lastname = e.target.lastname.value;
            const userType = e.target.userType.value;
    
            let statusValidator = validatorRegister(username, password, name, lastname, userType);
    
            if (statusValidator) {
                const userData: RegisterModel = {
                    "username": username,
                    "password": password,
                    "name": name, 
                    "lastname": lastname,
                    "type": userType
                }
                sendRegister(userData);
            }
        }
    }
      
    return(
        <main className="h-full w-full">
            <Zoom className="w-full h-full flex justify-center items-center">
                <div className="bg-gray-550 min-h-fit h-fit w-45 rounded-2xl shadow-xl flex flex-col items-center px-6 py-5">
                    <header className="flex flex-col items-center w-60 mb-6">
                        <a href="/"><img className="h-16" src="/assets/logo.png" alt="logo" /></a>
                        <a href="/"><h1 className="text-blue-500 text-3xl font-lexend font-bold text-center"><span className="text-red-500">I</span>nterface <span className="text-red-500">C</span>hange <span className="text-red-500">M</span>onitor</h1></a>
                    </header>
                    {modo == "login" && <h2 className="font-lexend text-blue-500 font-semibold text-xl w-full text-center mb-2">Inicio de Sesión</h2>}
                    {modo == "register" && <h2 className="font-lexend text-blue-500 font-semibold text-xl w-full text-center mb-1">Registro</h2>}
                    {modo == "login" && <div className="h-1 w-40 bg-blue-500 mb-3 rounded-full"></div>}
                    {modo == "register" && <div className="h-1 w-30 bg-blue-500 mb-3 rounded-full"></div>}
                    <form onSubmit={formHandler} className="flex flex-col gap-1 w-80 min-w-fit max-md:gap-2">
                        <div className="flex flex-col w-full">
                            <div className="flex flex-row w-full px-4 max-md:flex-col">
                                <label htmlFor="user" className="w-50 bg-blue-500 md:rounded-l-md py-2 font-lexend text-white text-center px-2 max-md:w-full max-md:rounded-t-md">Usuario</label>
                                <input type="text" name="user" id="user" placeholder="Nombre de Usuario" className="outline-none md:rounded-r-md w-full px-2 max-md:py-1 max-md:rounded-b-md" />
                            </div>
                            <small id="alertUser" className="px-6 font-lexend font-light text-red-100 hidden my-1">Es obligatorio un usuario</small>
                            <small id="alertRepeatUser" className="px-6 font-lexend font-light text-red-100 hidden my-1">Usuario inválido</small>
                            <small id="alertUserRegex" className="px-6 font-lexend font-light text-red-100 text-xs hidden my-1">El usuario no puede contener caracteres especiales (@, :, ;, /, \, -, (), "")</small>
                        </div>
                        <div className="flex flex-col w-full">
                            <div className="flex flex-row w-full px-4 max-md:flex-col">
                                <label htmlFor="password" className="w-50 bg-blue-500 md:rounded-l-md py-2 font-lexend text-white text-center px-2 max-md:w-full max-md:rounded-t-md">Contraseña</label>
                                <div className="flex flex-row w-full">
                                    <input type="password" name="password" id="password" placeholder="Contraseña" className="w-full px-2 outline-none max-md:py-1" />
                                    <button type="button" id="viewPassword-one" className="p-1 bg-white md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('password')}}>    
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                                            <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                            <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                        </svg>
                                    </button>
                                    <button type="button" id="hiddenPassword-one" className="p-1 hidden bg-white md:rounded-r-md max-md:rounded-br-md" onClick={() => {viewPassword('password')}}>    
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye-slash" viewBox="0 0 16 16">
                                            <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z"/>
                                            <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
                                            <path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12z"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <small id="alertPassword" className="px-6 font-lexend font-light text-red-100 hidden">Es obligatorio una contraseña</small>
                        </div>
                        {modo == "register" &&
                            <div className="flex flex-col w-full">
                                <div className="flex flex-row w-full px-4 max-md:flex-col">
                                    <label htmlFor="name" className="w-50 bg-blue-500 md:rounded-l-md py-2 font-lexend text-white text-center px-2 max-md:w-full max-md:rounded-t-md">Nombre</label>
                                    <input type="text" name="name" id="name" placeholder="Nombre" className="outline-none md:rounded-r-md w-full px-2 max-md:py-1 max-md:rounded-b-md" />
                                </div>
                                <small id="alertName" className="px-6 font-lexend font-light text-red-100 hidden">Es obligatorio un nombre</small>
                                <small id="alertNameRegex" className="px-6 font-lexend font-light text-red-100 text-xs hidden my-1">El nombre no puede contener caracteres especiales (@, :, ;, /, \, -, (), "")</small>
                            </div>
                        }
                        {modo == "register" &&
                            <div className="flex flex-col w-full">
                                <div className="flex flex-row w-full px-4 max-md:flex-col">
                                    <label htmlFor="lastname" className="w-50 bg-blue-500 md:rounded-l-md py-2 font-lexend text-white text-center px-2 max-md:w-full max-md:rounded-t-md">Apellido</label>
                                    <input type="text" name="lastname" id="lastname" placeholder="Apellido" className="outline-none md:rounded-r-md w-full px-2 max-md:py-1 max-md:rounded-b-md" />
                                </div>
                                <small id="alertLastname" className="px-6 font-lexend font-light text-red-100 hidden">Es obligatorio un apellido</small>
                                <small id="alertLastnameRegex" className="px-6 font-lexend font-light text-red-100 text-xs hidden my-1">El apellido no puede contener caracteres especiales (@, :, ;, /, \, -, (), "")</small>
                            </div>
                        }
                        {modo == "register" && 
                            <div className="flex flex-col w-full">
                                <div className="flex flex-row w-full px-4 max-md:flex-col">
                                    <label htmlFor="userType" className="w-50 bg-blue-500 md:rounded-l-md py-2 font-lexend text-white text-center px-2 max-md:w-full max-md:rounded-t-md">Tipo</label>
                                    <select name="userType" id="userType" className="outline-none w-full px-2 bg-white font-lexend font-normal text-black-500 max-md:py-1 md:rounded-r-md max-md:rounded-b-md">
                                        <option value="">----</option>
                                        <option value="user">Usuario Común</option>
                                        <option value="admin">Usuario Administrador</option>
                                    </select>
                                </div>
                                <small id="alertUserType" className="px-6 font-lexend font-light text-red-100 hidden">Es obligatorio seleccionar un tipo de usuario</small>
                            </div>
                        }
                        {modo == "login" && 
                            <div className="flex flex-col justify-center items-center mt-4 mb-4">
                                <button type="submit" className="w-fit font-lexend font-semibold text-white bg-blue-500 rounded-full px-12 py-2 transition-all duration-300 ease-in-out hover:bg-blue-800">Iniciar Sesión</button>
                                <small id="alertInvalidUser" className="px-6 text-center font-lexend font-light text-red-100 hidden">Usuario o contraseña incorrecta</small>
                            </div>
                        }
                        {modo == "register" && 
                            <div className="flex justify-center mt-4 mb-4">
                                <button type="submit" className="w-fit font-lexend font-semibold text-white bg-blue-500 rounded-full px-12 py-2 transition-all duration-300 ease-in-out hover:bg-blue-800">Register</button>
                            </div>
                        }
                        {modo == "login" && <p className="text-center text-sm font-lexend font-light text-black-500">¿Has olvidado tu contraseña? <a href="/forgotPassword" className="font-lexend font-normal text-blue-500 hover:underline">Solicita tu cambio de contraseña</a></p>}
                        {modo == "login" && <p className="text-center text-sm font-lexend font-light text-black-500">¿No estás registrado? <a href="/register" className="font-lexend font-normal text-blue-500 hover:underline">Registrate</a></p>}
                        {modo == "register" && <p className=" text-center text-sm font-lexend font-light text-black-500">¿Ya estás registrado? <a href="/" className="font-lexend font-normal text-blue-500 hover:underline">Inicia Sesión</a></p>}
                    </form>
                </div>
            </Zoom>
        </main>
    );
}