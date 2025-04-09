# Movie recommender!

### För att kunna köras måste du ladda ner ml-latest från länken nedan, mappen ska läggas så filstrukturen blir Film/ml-latest
### Länk: https://files.grouplens.org/datasets/movielens/ml-latest.zip

- Eftersom denna algorithm jämför mellan taggar och genres så har en del filmer filtrerats som inte innehåller taggar.
- Om du använder rating för att filtera så kommer den ta bort även filmer som inte har mer än 25 omdömen.
- Du kan ange endast en film men om du väljer fler filmer kommer den ta ett euklidiskt avstånd mellan varje film, summera dem och ta kortaste avstånd.
- När du börjar skriva in i searchbar kommer det komma förslag på filmer. Pga optimering laddas inte alla förslag när du inte skrivit något.
- ratings.csv i ml-latest är väldigt stor och har därför en bantad version i Film/ratings.csv
- Genres är inkluderad som taggar och beräknas som likvärdiga

### Min process:
>Jag tänkte att för just denna modell så kommer det aldrig vara någon ny indata utan all data jag kommer jobba med är känd data, alltså är det egentligen inget jag ska "förutse" utan ta den mest likartade filmer som jag redan känner till. Alltså blir det en form av overfit på träningsdatan. Eftersom jag ville jobba med taggar så valde jag att använda collaborative-filtering. Jag tyckte att cosinus-likhet och ta det euklidiska avståndet gav exakt samma svar för de 5 filmer. Därför valde jag euklidiskt avstånd som modell eftersom jag ville summera avstånden för fler filmer och ta det kortaste. Även om det skulle likna samma resultat som cosinus-likhet så var det lättare att förstå att summera avstånd. Jag ville från början kunna förutse mer ökända filmer men det blir svårt att få tag i dem om de saknar tags eller rätt antal ratings. Därför valde jag att endast ha dem som bara har tags(vilket är rimligt). Det var också kul att få användning av links.csv och kombinera det med lite scraping för att få filmomslag med referens. Sedan kan man alltid jobba lite med utsidan men av erfarenhet kan det ta enormt med tid vilket jag inte har just nu så använde en enklare dcc.markdown att skriva i när man kommer in på hemsidan. Pillade lite med themes men inget märkvärdigt. Den största svårigheten har varit indexeringsproblem från movieId till matrisindex och tillbaka. Man skulle kunna göra det på många sett men det som hjälpte mig var min translate() som räddade mig från många problem. Väldigt enkel funktion men att slippa ha saker i huvudet hjälpte mycket.

