<?php

declare(strict_types=1);

namespace Src\Groups\App\Requests;

use Illuminate\Foundation\Http\FormRequest;

class AddUserToGroupRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'users' => ['required', 'array'],
            'users.*' => ['integer', 'exists:users,id'],
        ];
    }

    /**
     * @return array<int, int>
     */
    public function toIdArray(): array
    {
        /** @var array<int, int> $array */
        $array = $this->array('users');

        return $array;
    }
}
