// src/env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  // 这里的名字必须和 .env 文件里的完全一样
  readonly VITE_API_BASE_URL: string
  readonly VITE_AMAP_WEB_KEY: string
  readonly VITE_AMAP_WEB_JS_KEY: string

}

interface ImportMeta {
  readonly env: ImportMetaEnv
}