# LunaGC-7.0.0 WIP

[Deutsch (German)](README.de-de.md)

## 維護者的說明
可能會偶爾更新到最新版本，取決於我的心情和情況。當然，我在 [GitLab](https://gitlab.com/kitkat-multiverse/genshin-protocol) 上發佈協議緩衝區定義。

## 更新版本的 Grasscutters，實現了一些新功能。
舊的 LunaGC Discord https://discord.gg/7D5gkyJR5Y （不要在那裡尋求支持，因為它已被他人接管，請改為在此存儲庫中創建問題）

PS 的功能和特性不保證，請自己嘗試看看什麼有效，什麼無效。

如果您想/能夠做出貢獻...

# 閱讀[手冊](handbook.md)！

# 設置指南
- 閱讀下面的內容，足以讓伺服器和客戶端啟動並運行。

## 主要要求

- 獲取 [Java 17](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
- 獲取 [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- 獲取 [NodeJS](https://nodejs.org/dist/v20.15.0/node-v20.15.0-x64.msi)（用於手冊生成）
- 獲取遊戲版本 REL7.0.0
- 確保安裝了 Java 並設置了環境變量。
- 構建伺服器（參考本指南中的"編譯伺服器"。）
- 下載[資源](https://github.com/fjyczcr/LunaGC-Resources)，在下載的 LunaGC 文件夾中新建一個名為 `resources` 的文件夾，然後在該新文件夾中提取資源。
- 將 useEncryption、Questing 和 useInRouting 設置為 false（默認應該是 false，如果不是則更改）
- [修補遊戲](#修補遊戲)
- 啟動伺服器和遊戲，確保也在 LunaGC 控制台中創建帳戶！
- 玩得開心（或不）

### 修補遊戲
- 將 `patch/Astrolabe.dll` 複製到遊戲資料夾 `GenshinImpact_Data/Plugins` 中。請先備份 plugins 資料夾內原有的 `Astrolabe.dll`。
- 若想自行建置，請先複製 [hk4e-patch-universal](https://github.com/fjyczcr/hk4e-patch-universal) 專案，安裝 [**Rust**](https://rust-lang.org/learn/get-started/) 與 **Cargo**（隨 rustup 一同提供），然後執行 `cargo build --release`，最後將 `target/release` 目錄下的 DLL 重新命名為 `Astrolabe.dll`。

### 入門

- 克隆存儲庫（首先安裝 [Git](https://git-scm.com)）

  ```
  git clone --recurse-submodules https://github.com/fjyczcr/LunaGC.git
  ```

- 現在您可以繼續執行以下步驟。


### 編譯伺服器

**要求**:

[Java Development Kit 17 | JDK](https://oracle.com/java/technologies/javase/jdk17-archive-downloads.html) 或更高版本

- **附註**：在某些系統上手冊生成可能會失敗。要禁用手冊生成，請在 `gradlew jar` 命令中附加 `-PskipHandbook=1`。

- **對於 Windows**:

  ```shell
  .\gradlew.bat
  .\gradlew.bat jar
  ```

- **對於 Linux**:

  ```bash
  chmod +x gradlew
  ./gradlew
  ./gradlew jar
  ```

### 您可以在項目根文件夾中找到輸出 JAR。

### 手動編譯手冊

```shell
./gradlew generateHandbook
```

## 故障排除

- 確保將 useEncryption 和 useInRouting 都設置為 false，否則您可能會遇到錯誤。
- 要使用 Windy，請確保將您的 luac 文件放在 `C:\Windy` 中（如果該文件夾不存在，請創建該文件夾）
- 如果您遇到與 MongoDB 連線超時相關的錯誤，請檢查 mongodb 服務是否正在運行。在 Windows 上：按下 Windows 鍵和 R，然後輸入 `services.msc`，尋找 mongodb 服務，如果尚未啟動，請右鍵點擊並選擇啟動。在 Linux 上，您可以使用 `systemctl status mongod` 來查看是否正在運行，如果沒有運行，請輸入 `systemctl start mongod`。然而，如果在 Linux 上收到錯誤 14，請更改 mongodb 資料夾及 .sock 檔案的擁有者（`sudo chown -R mongodb:mongodb /var/lib/mongodb` 和 `sudo chown mongodb:mongodb /tmp/mongodb-27017.sock`），然後再嘗試啟動服務。

## 致謝

proto 存儲庫 [hk4e-protos](https://gitlab.com/kitkat-multiverse/genshin-protocol)

補丁存儲庫 [hk4e-patch-universal](https://github.com/kitkat033/hk4e-patch-universal)
