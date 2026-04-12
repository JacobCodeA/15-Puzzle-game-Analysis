$StatsFilenameRegex = '^[a-zA-Z0-9]+_[0-9]+_[0-9]+_[a-zA-Z]+_[a-zA-Z]+_stats.txt$'

$Results = Get-ChildItem -File | Where-Object { $_.Name -match $StatsFilenameRegex } | ForEach-Object {
    
$SplitFilename = $_.BaseName.Split("_")

$strategy = $SplitFilename[3]
$depth = [int]$SplitFilename[1]
$param = $SplitFilename[4]

$content = Get-Content $_.Name

    [PSCustomObject]@{
	Strategy     = $strategy
        Depth        = $depth
        Param        = $param
        Value1       = $content[0]
        Value2       = $content[1]
        Value3       = $content[2]
        Value4       = $content[3]
        Value5       = $content[4]
    }
}

$Results | Export-Csv -Path "results.csv" -NoTypeInformation -Encoding UTF8