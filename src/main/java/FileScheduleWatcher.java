import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.concurrent.Executors;

public class FileScheduleWatcher extends FileWatcher implements Runnable{
    public FileScheduleWatcher(Path targetFolder, Path resultFolder) {
        super(targetFolder, resultFolder);
    }

    @Override
    public void startWatch() {
        //executors
    }

    public static void main(String[] args) {
        try{
            Path targetFolder = Paths.get(args[0]);
            Path resultFolder = Paths.get(args[1]);
            FileWatcher fileWatcher = new FileScheduleWatcher(targetFolder,resultFolder);
            //1시간마다 실행
            Executors.newSingleThreadExecutor();
            fileWatcher.run();
        } catch (ArrayIndexOutOfBoundsException arrayIndexOutOfBoundsException) {
            System.out.println("Not Enough Values");
        }
    }

    @Override
    public void run() {
        try {
            Files.walkFileTree(targetFolder, new FileVisitor<Path>() {
                @Override
                public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
                    Path resultDir = Paths.get(resultFolder.toString() + dir.toString().replace(targetFolder.toString(), ""));
                    if (!Files.exists(resultDir)) {
                        Files.createDirectories(resultDir);
                    }
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    if ((!file.toString().contains(".part")) && (!file.toString().contains(".encrypted"))) {
                        Path resultFile = Paths.get(resultFolder.toString() + file.toString().replace(targetFolder.toString(), ""));
                        Files.move(file, resultFile, copyOptions);
                    }
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
                    return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            System.out.println("폴더 순회중 오류가 발생했습니다.");
        }
    }

}
