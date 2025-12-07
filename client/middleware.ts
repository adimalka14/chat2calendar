import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // For now, we'll handle auth client-side
  // This middleware can be extended for server-side auth validation
  return NextResponse.next()
}

export const config = {
  matcher: ["/chat/:path*", "/api/:path*"],
}
