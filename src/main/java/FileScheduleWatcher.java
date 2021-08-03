import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class FileScheduleWatcher extends FileWatcher implements Runnable {
    ScheduledExecutorService scheduledExecutorService;
    int delayHour;
    boolean running;

    public FileScheduleWatcher(Path targetFolder, Path resultFolder, List<String> ignoreExtList) {
        this(targetFolder, resultFolder, ignoreExtList, 1);
    }

    public FileScheduleWatcher(Path targetFolder, Path resultFolder, List<String> ignoreExtList, int delayHour) {
        super(targetFolder, resultFolder, ignoreExtList);
        this.scheduledExecutorService = Executors.newSingleThreadScheduledExecutor();
        this.running = false;
        this.delayHour = delayHour;
    }


    private Path getResultPath(Path path) {
        return Paths.get(resultFolder.toString() + path.toString().replace(targetFolder.toString(), ""));
    }

    @Override
    public void startWatch() {
        if (running) {
            throw new IllegalStateException();
        }
        running = true;
        scheduledExecutorService.scheduleWithFixedDelay(this, 0, 1, TimeUnit.SECONDS);
    }

    @Override
    public void run() {
        try {
            Files.walkFileTree(targetFolder, new FileVisitor<Path>() {
                @Override
                public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
                    Path resultDir = getResultPath(dir);
                    if (!Files.exists(resultDir)) {
                        Files.createDirectories(resultDir);
                    }
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    Path resultFile = getResultPath(file);
                    if (ignoreExtList.stream().noneMatch(s -> file.toString().contains(s))) {
                        CopyOption[] copyOptions = new CopyOption[]{StandardCopyOption.REPLACE_EXISTING};
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
                    BasicFileAttributes attributes = Files.readAttributes(dir, BasicFileAttributes.class);
                    if ((!Files.isSameFile(dir, targetFolder))) {
                        Files.delete(dir);
                    }
                    return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            System.out.println("폴더 순회중 오류가 발생했습니다.");
        }
    }
}
