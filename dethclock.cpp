#include <iostream>
#include <unordered_map>
#include <string>
#include <ctime>
#include <iomanip>

struct LifeExpectancy {
    double male;
    double female;
};

static const std::unordered_map<std::string, LifeExpectancy> EXPECTANCY = {
    {"Global Average", {70.8, 75.9}},
    {"Japan", {81.5, 87.6}},
    {"Switzerland", {81.8, 85.5}},
    {"South Korea", {79.3, 85.4}},
    {"Singapore", {81.0, 85.7}},
    {"Spain", {80.7, 86.2}},
    {"Italy", {81.2, 85.6}},
    {"Australia", {81.2, 85.3}},
    {"Iceland", {80.5, 84.8}},
    {"Israel", {79.9, 84.1}},
    {"Sweden", {80.8, 84.7}},
    {"France", {79.8, 85.8}},
    {"Norway", {80.5, 84.4}},
    {"Malta", {79.8, 84.5}},
    {"Netherlands", {80.1, 83.8}},
    {"Austria", {79.0, 84.1}},
    {"Finland", {78.8, 84.5}},
    {"New Zealand", {80.2, 83.5}},
    {"Ireland", {79.9, 83.5}},
    {"United Kingdom", {79.2, 82.9}},
    {"Belgium", {79.2, 84.1}},
    {"Germany", {78.7, 83.4}},
    {"Canada", {80.0, 84.0}},
    {"Luxembourg", {79.8, 84.6}},
    {"Greece", {78.4, 83.8}},
    {"Portugal", {78.9, 84.9}},
    {"Slovenia", {78.3, 84.3}},
    {"Denmark", {78.9, 82.9}},
    {"Cyprus", {79.2, 83.1}},
    {"United States", {76.4, 81.2}},
    {"Czech Republic", {76.1, 82.1}},
    {"Chile", {77.2, 82.4}},
    {"Costa Rica", {77.8, 82.2}},
    {"Poland", {74.0, 81.6}},
    {"Estonia", {74.4, 82.4}},
    {"Panama", {76.2, 81.8}},
    {"Turkey", {76.2, 81.3}},
    {"Albania", {76.9, 80.9}},
    {"Croatia", {75.4, 81.2}},
    {"Uruguay", {74.5, 81.2}},
    {"Cuba", {77.2, 81.9}},
    {"Argentina", {73.0, 79.8}},
    {"Lebanon", {77.4, 81.3}},
    {"China", {75.1, 80.5}},
    {"Brazil", {72.2, 79.4}},
    {"Thailand", {72.6, 80.0}},
    {"Iran", {74.2, 77.6}},
    {"Mexico", {72.1, 77.7}},
    {"Colombia", {73.0, 79.0}},
    {"Algeria", {75.9, 78.3}},
    {"Tunisia", {74.2, 78.7}},
    {"Ecuador", {74.1, 79.5}},
    {"Sri Lanka", {73.1, 79.2}},
    {"Morocco", {74.0, 77.3}},
    {"Peru", {73.7, 79.1}},
    {"Jordan", {72.7, 76.1}},
    {"Armenia", {71.6, 78.9}},
    {"Vietnam", {71.7, 80.9}},
    {"Venezuela", {69.2, 77.2}},
    {"Egypt", {70.2, 74.1}},
    {"Libya", {70.2, 75.9}},
    {"Paraguay", {71.7, 77.2}},
    {"Ukraine", {67.0, 76.9}},
    {"Philippines", {67.5, 75.0}},
    {"El Salvador", {70.4, 78.1}},
    {"Honduras", {72.3, 76.9}},
    {"Guatemala", {71.2, 76.8}},
    {"Bolivia", {67.5, 72.4}},
    {"Nepal", {69.0, 71.9}},
    {"Nicaragua", {72.4, 78.1}},
    {"Bangladesh", {71.2, 74.2}},
    {"Cambodia", {67.1, 71.1}},
    {"India", {68.4, 70.7}},
    {"Pakistan", {66.1, 68.4}},
    {"Myanmar", {64.8, 69.8}},
    {"Kenya", {61.4, 66.2}},
    {"Ghana", {62.4, 64.7}},
    {"Tanzania", {63.1, 67.3}},
    {"Uganda", {61.7, 65.4}},
    {"Rwanda", {67.3, 71.7}},
    {"Ethiopia", {64.9, 68.9}},
    {"Madagascar", {64.5, 67.8}},
    {"Senegal", {66.3, 70.1}},
    {"Mali", {57.3, 59.8}},
    {"Burkina Faso", {59.3, 61.4}},
    {"Niger", {60.4, 62.1}},
    {"Chad", {52.5, 55.4}},
    {"Nigeria", {53.4, 55.7}},
    {"South Africa", {62.3, 68.5}},
    {"Zimbabwe", {59.3, 63.4}},
    {"Botswana", {66.1, 72.4}},
    {"Zambia", {61.2, 65.1}},
    {"Mozambique", {58.8, 64.2}},
    {"Angola", {59.3, 64.4}},
    {"Sierra Leone", {52.2, 55.7}},
    {"Central African Republic", {51.0, 55.7}}
};

LifeExpectancy get_expectancy(const std::string& country) {
    auto it = EXPECTANCY.find(country);
    if (it != EXPECTANCY.end()) {
        return it->second;
    }
    return EXPECTANCY.at("Global Average");
}

int main() {
    std::cout << "Death Clock (C++)" << std::endl;
    std::string birth_str;
    std::cout << "Enter birth date (DD/MM/YYYY): ";
    std::getline(std::cin, birth_str);

    std::string gender;
    std::cout << "Gender (Male/Female): ";
    std::getline(std::cin, gender);

    std::string country;
    std::cout << "Country: ";
    std::getline(std::cin, country);

    std::tm birth_tm{};
    if (!strptime(birth_str.c_str(), "%d/%m/%Y", &birth_tm)) {
        std::cerr << "Invalid date format" << std::endl;
        return 1;
    }
    std::time_t birth_time = std::mktime(&birth_tm);

    LifeExpectancy ex = get_expectancy(country);
    double lifespan_years = (gender == "Male" ? ex.male : ex.female);
    std::time_t death_time = birth_time + static_cast<time_t>(lifespan_years * 365.25 * 24 * 3600);

    std::time_t now = std::time(nullptr);
    double seconds_left = std::difftime(death_time, now);
    if (seconds_left <= 0) {
        std::cout << "Your time has already expired!" << std::endl;
        return 0;
    }

    double days_left = seconds_left / 86400.0;
    double hours_left = seconds_left / 3600.0;
    double years_left = days_left / 365.25;

    std::cout << "Estimated death date: "
              << std::put_time(std::localtime(&death_time), "%d/%m/%Y %H:%M:%S")
              << std::endl;
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Time remaining: " << years_left << " years (" << days_left
              << " days)" << std::endl;

    long sleep_hours = static_cast<long>(hours_left / 3);
    long meals = static_cast<long>(days_left * 3);
    long work_hours = static_cast<long>(days_left * 8);
    long tv_episodes = static_cast<long>(hours_left);
    long workouts = static_cast<long>(days_left / 2);

    std::cout << "Insights:\n";
    std::cout << "  ~" << sleep_hours << " hours of sleep left\n";
    std::cout << "  ~" << meals << " meals remaining\n";
    std::cout << "  ~" << work_hours << " work hours left\n";
    std::cout << "  ~" << tv_episodes << " TV episodes to watch\n";
    std::cout << "  ~" << workouts << " workouts remaining" << std::endl;

    return 0;
}
