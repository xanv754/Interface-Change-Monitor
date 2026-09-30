import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { PATHS } from "@/constants/paths";

export function middleware(request: NextRequest) {
  const hasSession = request.cookies.get("token");
  if (!hasSession && request.nextUrl.pathname !== PATHS.LOGIN) {
    return NextResponse.redirect(new URL(PATHS.LOGIN, request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|icon.png|public/).*)"],
};
