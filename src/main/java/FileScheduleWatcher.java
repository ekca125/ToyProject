import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class FileScheduleWatcher extends FileWatcher implements Runnable {
    private ScheduledExecutorService scheduledExecutorService;
    private int delayHour;
    private boolean running;

    public FileScheduleWatcher(Path targetFolder, Path resultFolder, List<String> ignoreExtList) {
        this(targetFolder, resultFolder, ignoreExtList, 1);
    }

    public FileScheduleWatcher(Path targetFolder, Path resultFolder, List<String> ignoreExtList, int delayHour) {
        super(targetFolder, resultFolder, ignoreExtList);
        this.running = false;
        this.scheduledExecutorService = Executors.newSingleThreadScheduledExecutor();
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
        scheduledExecutorService.scheduleWithFixedDelay(this, 0, delayHour, TimeUnit.HOURS);
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
                    if ((!Files.isSameFile(dir, targetFolder))) {
                        try {
                            Files.delete(dir);
                        }
                        catch (IOException ignored){
                            //파일을 다운로드 하고 있어서 디렉토리가 비어있지 않은 경우
                        }
                    }
                    return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("폴더 순회중 오류가 발생했습니다.");
        }
    }
}
