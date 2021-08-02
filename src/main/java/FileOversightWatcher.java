import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;

public class FileOversightWatcher extends FileWatcher{
    public FileOversightWatcher(Path targetFolder, Path resultFolder) {
        super(targetFolder, resultFolder);
    }

    public void startWatch(){
        try (WatchService watchService = FileSystems.getDefault().newWatchService();){
            targetFolder.register(watchService, StandardWatchEventKinds.ENTRY_CREATE);
            while(true){
                WatchKey changeKey = watchService.take();
                List<WatchEvent<?>> watchEvents = changeKey.pollEvents();
                for(WatchEvent<?> watchEvent:watchEvents){
                    WatchEvent<Path> pathEvent=(WatchEvent<Path>) watchEvent;
                    moveFile(pathEvent.context());
                }
                changeKey.reset();
            }
        } catch (NullPointerException e){
            System.out.println("타겟폴더 혹은 결과폴더가 없습니다.");
        }
        catch (IOException e) {
            System.out.println("파일처리중 오류가 발생했습니다.");
        } catch (InterruptedException e) {
            System.out.println("사용자의 입력에 의해 중단되었습니다.");
        }
    }
}
