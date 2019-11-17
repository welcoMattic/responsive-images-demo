<?php

namespace App\Service;

use League\Glide\Server;
use League\Glide\ServerFactory;
use League\Glide\Responses\SymfonyResponseFactory;

class Glide
{
    protected $server;
    protected $filters;

    public function __construct(array $serverConfig, array $filters)
    {
        $this->server = ServerFactory::create([
            'response' => new SymfonyResponseFactory(),
            'source' => $serverConfig['source_path'],
            'cache' => $serverConfig['cache_path'],
        ]);

        $this->filters = $filters;
    }

    public function getServer(): Server
    {
        return $this->server;
    }

    public function getFilters(): array
    {
        return $this->filters;
    }
}
