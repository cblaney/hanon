#include "server.hpp"

int main(int argc, char* argv[])
{

    auto const address = net::ip::make_address("0.0.0.0");
    auto const port = static_cast<unsigned short>(2000);
    auto const threads = 1;

    // The io_context is required for all I/O
    net::io_context ioc{threads};

    // Create and launch a listening port
    std::shared_ptr<Server> server = std::make_shared<Server>(ioc, address, port);
    server->run();

    std::vector<std::thread> v;
    v.reserve(threads);
    for(auto i = threads; i > 0; --i)
        v.emplace_back(
        [&ioc]
        {
            ioc.run();
        });

    while(1)
    {
        std::string msg;
        std::getline(std::cin, msg);
        server->send(msg);
        std::cout << msg.length() << std::endl;
    }

    for(auto& t : v)
        t.join();

    return EXIT_SUCCESS;
}