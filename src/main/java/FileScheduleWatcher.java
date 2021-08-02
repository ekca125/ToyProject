import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;

public class FileScheduleWatcher extends FileWatcher {
    public FileScheduleWatcher(Path targetFolder, Path resultFolder) {
        super(targetFolder, resultFolder);
    }

    public static void main(String[] args) {
        //args 사용

    }

    @Override
    public void startWatch() {
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
