 library(tidyr)
 library(readr)
 
 #WILL INCLUDE OUTPUT SO NO NEED TO RUN UNLESS SOMETHING WENT TERRIBLY WRONG
 
 # df <- read.csv("events-07735c1a.csv", header = FALSE)
 #  Error in file(file, "rt") : cannot open the connection
 #  In addition: Warning message:
 #    In file(file, "rt") :
 #    cannot open file 'events-07735c1a.csv': No such file or directory
 
 # had to redirect main console to different folder 
  setwd("/Users/brandonlee/Documents/UBX_World/UBX-Data-With-Headers")
  
  #reformatting (separating the csv files)
  
  df <- read.csv("events-07735c1a.csv", header = FALSE)
 
  colnames(df) <- c("Combined")
  
  df_separated <- separate(df, col = Combined, into = c("ID", "RawName", "ActualEvent"), sep = "\\|")
  #Warning message:
 #   Expected 3 pieces. Missing pieces filled with `NA` in 220 rows [627, 628, 3159, 3160, 3161, 3162, 3163, 5673, 5674, 5675, 5676, 5677, 5678, 5679, 5680, 5681, 5682, 5683, 5684, 5686, ...]. 
  # View(df_separated)
  #View(df)
   write.csv(df_separated, "events_separated.csv", row.names = FALSE)
   

  events_separated <- read_csv("events_separated.csv")
  # Rows: 12035 Columns: 3                                                                                    
  # ── Column specification ──────────────────────────────────────────────────────────────────────────────────
  # Delimiter: ","
  # chr (3): ID, RawName, ActualEvent
  # 
  # ℹ Use `spec()` to retrieve the full column specification for this data.
  # ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.
 
 df <- read.csv("matches-3b9987aa.csv", header = FALSE)
View(df)
colnames(df) <- c("Combined")
df_separated <- separate(df, col = Combined, into = c("ID", "TournamentID", "EventID", "ActualEvent", "Player1Team1Id", "Player2Team1Id", "Player1Team2Id", "Player2Team2Id", "Team1Set1Score", "Team2Set1Score", "Team1Set2Score", "Team2Set2Score", "Team1Set3Score", "Team2Set3Score", "StartDate|EndDate", sep = ("\\|")))
# Warning message:
#   Expected 16 pieces. Additional pieces discarded in 635033 rows [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, ...]. 
# View(df_separated)
write.csv(df_separated, "matches_separated.csv", row.names = FALSE)

#Player Separated Data
df <- read.csv("players-0b805c0a.csv", sep = "|", stringsAsFactors = FALSE)
write.csv(df, "players_separated.csv", row.names = FALSE)

#Tournament data separated
df <- read.csv("tournaments-e7f14f71.csv", sep = "|", stringsAsFactors = FALSE)
write.csv(df, "tournaments_separated.csv", row.names = FALSE)

df <- read.csv("venues-d2c96ec1.csv", sep = "|", stringsAsFactors = FALSE)
write.csv(df, "venues_separated.csv", row.names = FALSE)

# snippet for giving Tier Grades

df <- df %>%
   mutate(Tier = case_when(
             Label == "International Challenge" ~ "Grade B",
            Label == "International Series" ~ "Grade B", 
             Label == "Future Series" ~ "Grade B",
             TRUE ~ Tier
         ))




