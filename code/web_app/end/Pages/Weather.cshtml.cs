using System.Net.Http.Headers;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Identity.Web;

namespace pythonaspnetapp.Pages;

[AuthorizeForScopes(Scopes=new string[]{"api://<the CLIENT ID of your API App Registration>/Weather.Read"})]
public class WeatherModel : PageModel
{
    private readonly ILogger<WeatherModel> _logger;

    private readonly ITokenAcquisition _tokenAcquisition;

    public WeatherModel(ILogger<WeatherModel> logger, ITokenAcquisition tokenAcquisition)
    {
        _logger = logger;
        _tokenAcquisition = tokenAcquisition;
    }

    public async Task OnGet()
    {
        var token = await _tokenAcquisition.GetAccessTokenForUserAsync(new []{"api://de2656e6-585f-4684-8e65-3ce50a7770a8/Weather.Read"});

        // Call a downstream API
        var httpClient = new HttpClient();
        httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

        var response = await httpClient.GetAsync("http://localhost:8000/api/weather/seattle");
        var content = await response.Content.ReadAsStringAsync();

        ViewData["weather"] = content;
    }
}
