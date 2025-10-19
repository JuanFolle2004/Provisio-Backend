<?php

declare(strict_types=1);

namespace Src\Products\Domain\Dtos;

class ProductDto
{
    public function __construct(
        public string $name,
        public int $group_id,
        public int $amount,
    ) {
    }
}
