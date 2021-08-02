import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;

public class FileWatcher {
    Path targetFolder;
    Path resultFolder;
    CopyOption[] copyOptions;

    public FileWatcher(Path targetFolder,Path resultFolder){
        copyOptions = new CopyOption[]{StandardCopyOption.REPLACE_EXISTING};
        try {
            this.targetFolder = targetFolder.toRealPath();
            this.resultFolder = resultFolder.toRealPath();
        }
        catch (IOException e) {
            this.targetFolder = null;
            this.resultFolder = null;
        }
    }

    public void startWatch(){
        try (WatchService watchService = FileSystems.getDefault().newWatchService();){
            targetFolder.register(watchService,StandardWatchEventKinds.ENTRY_CREATE);
            while(true){
                WatchKey changeKey = watchService.take();
                List<WatchEvent<?>> watchEvents = changeKey.pollEvents();
                for(WatchEvent<?> watchEvent:watchEvents){
                    WatchEvent<Path> pathEvent=(WatchEvent<Path>) watchEvent;

                    Path fileName = pathEvent.context();
                    Path filePath = Paths.get(this.targetFolder.toString(),fileName.toString());
                    Path resultFilePath = Paths.get(this.resultFolder.toString(),fileName.toString());

                    BasicFileAttributes basicFileAttributes = Files.readAttributes(filePath,BasicFileAttributes.class);
                    if((!fileName.toString().contains(".part"))&&(!basicFileAttributes.isDirectory())){
                        Files.move(filePath,resultFilePath,copyOptions);
                    }
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

    public static void main(String[] args) {
        try{
            Path targetFolder = Paths.get(args[0]);
            Path resultFolder = Paths.get(args[1]);
            FileWatcher fileWatcher = new FileWatcher(targetFolder,resultFolder);
            fileWatcher.startWatch();
        } catch (ArrayIndexOutOfBoundsException arrayIndexOutOfBoundsException) {
            System.out.println("Not Enough Values");
        }
    }
}
